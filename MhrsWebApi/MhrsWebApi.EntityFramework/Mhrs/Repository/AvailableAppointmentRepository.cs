using MhrsWebApi.Domain;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using static System.Runtime.InteropServices.JavaScript.JSType;

namespace MhrsWebApi.EntityFramework
{
    public class AvailableAppointmentRepository : IAvailableAppointmentRepository
    {
        private readonly MhrsDbContext _context;

        public AvailableAppointmentRepository(MhrsDbContext context)
        {
            _context = context;
        }

        public AvailableAppointment? GetAvailable(int departmentId, DateTime? date, string? timePreference)
        {
            var query = from available in _context.AvailableAppointments
                                 join booked in _context.UserAppointments
                                 on available.Id equals booked.AvailableAppointmentId into joined
                                 from subBooked in joined.DefaultIfEmpty()
                                 where subBooked == null // Sadece eşleşmesi olmayan (yani boş olan) randevular
                                 select available;

            query = query.Include(x => x.Department).Include(x => x.Doctor).AsQueryable();

            query = query.Where(w => w.DepartmentId == departmentId);

            query = query.Where(w => w.AppointmentDate > DateTime.Now);

            if (date != null)
                query = query.Where(w => w.AppointmentDate.Day == date.Value.Day && w.AppointmentDate.Month == date.Value.Month && w.AppointmentDate.Year == date.Value.Year);

            if (!string.IsNullOrEmpty(timePreference))
            {
                if (timePreference.ToLower() == "sabah")
                    query = query.Where(w => w.AppointmentDate.Hour < 12);
                else if (timePreference.ToLower() == "öğleden sonra")
                    query = query.Where(w => w.AppointmentDate.Hour >= 12 && w.AppointmentDate.Hour < 17);
                else if (TimeSpan.TryParse(timePreference, out TimeSpan exactTime))
                    query = query.Where(w => w.AppointmentDate.TimeOfDay == exactTime); // "14:00" gibi net bir saat geldiyse
            }
            
            return query.OrderBy(o => o.AppointmentDate).FirstOrDefault();
        } 
    }
}
