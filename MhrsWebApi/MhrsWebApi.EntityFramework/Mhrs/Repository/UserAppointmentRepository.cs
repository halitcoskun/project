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
    public class UserAppointmentRepository : IUserAppointmentRepository
    {
        private readonly MhrsDbContext _context;

        public UserAppointmentRepository(MhrsDbContext context)
        {
            _context = context;
        }

        public IQueryable<UserAppointment> GetQueryable()
        {
            return _context.UserAppointments.AsQueryable();
        }

        public List<UserAppointment> GetAllDateOfRange(Guid userId, DateTime? date)
        {
            var query = _context.UserAppointments.Include(x => x.AvailableAppointment).Include(x => x.AvailableAppointment!.Department).Include(x => x.AvailableAppointment!.Doctor)
                .AsQueryable();

            query = query.Where(w => w.UserId == userId);

            query = query.Where(w => w.AvailableAppointment!.AppointmentDate > DateTime.Now);

            try
            {
                if (date != null)
                    query = query.Where(w => w.AvailableAppointment!.AppointmentDate.Day == date.Value.Day && w.AvailableAppointment!.AppointmentDate.Month == date.Value.Month && w.AvailableAppointment!.AppointmentDate.Year == date.Value.Year);
            }
            catch
            {
            }

            return query.OrderBy(o => o.AvailableAppointment!.AppointmentDate).ToList();
        }


        public UserAppointment? Get(Guid userId, DateTime? date, string? timePreference)
        {
            var query = _context.UserAppointments.Include(x => x.AvailableAppointment).Include(x => x.AvailableAppointment!.Department).Include(x => x.AvailableAppointment!.Doctor)
                .AsQueryable();

            query = query.Where(w => w.UserId == userId);

            query = query.Where(w => w.AvailableAppointment!.AppointmentDate > DateTime.Now);

            try
            {
                if (date != null)
                    query = query.Where(w => w.AvailableAppointment!.AppointmentDate.Day == date.Value.Day && w.AvailableAppointment!.AppointmentDate.Month == date.Value.Month && w.AvailableAppointment!.AppointmentDate.Year == date.Value.Year);

                if (!string.IsNullOrEmpty(timePreference))
                {
                    if (timePreference.ToLower() == "sabah")
                        query = query.Where(w => w.AvailableAppointment!.AppointmentDate.Hour < 12);
                    else if (timePreference.ToLower() == "öğleden sonra")
                        query = query.Where(w => w.AvailableAppointment!.AppointmentDate.Hour >= 12 && w.AvailableAppointment!.AppointmentDate.Hour < 17);
                    else if (TimeSpan.TryParse(timePreference, out TimeSpan exactTime))
                        query = query.Where(w => w.AvailableAppointment!.AppointmentDate.TimeOfDay == exactTime); // "14:00" gibi net bir saat geldiyse
                }
            }
            catch
            {
            }

            return query.OrderBy(o => o.SystemDate).FirstOrDefault();
        }

        public bool Add(UserAppointment userAppointment)
        {
            _context.UserAppointments.Add(userAppointment);
            var resp = _context.SaveChanges();

            if (resp > 0)
                return true;

            return false;
        }

        public bool Remove(UserAppointment userAppointment)
        {
            _context.UserAppointments.Remove(userAppointment);
            var resp = _context.SaveChanges();

            if (resp > 0)
                return true;

            return false;
        }

        public UserAppointment? Get(int departmentId, DateTime? time, Guid userId)
        {
            var query = _context.UserAppointments.Include(x => x.AvailableAppointment)
                .AsQueryable();

            query = query.Where(w => w.UserId == userId && w.AvailableAppointment!.DepartmentId == departmentId);

            query = query.Where(w => w.AvailableAppointment!.AppointmentDate > DateTime.Now);

            try
            {
                if (time != null)
                    query = query.Where(w => w.AvailableAppointment!.AppointmentDate.Day == time.Value.Day && w.AvailableAppointment!.AppointmentDate.Month == time.Value.Month && w.AvailableAppointment!.AppointmentDate.Year == time.Value.Year);
            }
            catch
            {
            }

            return query.OrderBy(o => o.SystemDate).FirstOrDefault();
        }
    }
}
