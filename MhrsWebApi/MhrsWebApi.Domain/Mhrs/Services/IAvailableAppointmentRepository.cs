using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MhrsWebApi.Domain
{
    public interface IAvailableAppointmentRepository
    {
        public AvailableAppointment? GetAvailable(int departmentId, DateTime? time, string? timePreference);
    }
}
