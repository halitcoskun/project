using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MhrsWebApi.Domain
{
    public interface IUserAppointmentRepository
    {
        public IQueryable<UserAppointment> GetQueryable();

        public List<UserAppointment> GetAllDateOfRange(Guid userId, DateTime? date);

        public UserAppointment? Get(Guid userId, DateTime? date, string? timePreference);

        public bool Add(UserAppointment userAppointment);

        public bool Remove(UserAppointment userAppointment);

        public UserAppointment? Get(int departmentId, DateTime? time, Guid userId);
    }
}
