using MhrsWebApi.Domain;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MhrsWebApi.Application
{
    public class AppointmentHelper
    {
        private readonly IAvailableAppointmentRepository _availableAppointmentRepository;
        private readonly IUserAppointmentRepository _userAppointmentRepository;
        private readonly IDepartmentRepository _departmentRepository;

        public AppointmentHelper(IAvailableAppointmentRepository availableAppointmentRepository, IDepartmentRepository departmentRepository, IUserAppointmentRepository userAppointmentRepository)
        {
            _availableAppointmentRepository = availableAppointmentRepository;
            _departmentRepository = departmentRepository;
            _userAppointmentRepository = userAppointmentRepository;
        }

        public AvailableAppointment? GetAvailableAppointment(string departmentName, string? availableDate, string? userId, string? timeReference)
        {
            DateTime? date = null;

            try
            {
                if (!string.IsNullOrEmpty(availableDate))
                    date = DateTime.Parse(availableDate);
            }
            catch
            {
            }

            var appointment = _userAppointmentRepository.Get(Guid.Parse(userId!), date, timeReference);

            if (appointment != null)
                return null;

            var department = _departmentRepository.Get(departmentName);

            if (department == null)
                return null;

            var availableAppointment = _availableAppointmentRepository.GetAvailable(department!.Id, date, timeReference);

            return availableAppointment;
        }
    }
}
