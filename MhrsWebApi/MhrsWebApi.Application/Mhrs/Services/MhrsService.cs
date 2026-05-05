using MhrsWebApi.Domain;

namespace MhrsWebApi.Application
{
    public class MhrsService : IMhrsService
    {
        private readonly IAvailableAppointmentRepository _availableAppointmentRepository;
        private readonly IUserAppointmentRepository _userAppointmentRepository;
        private readonly IDepartmentRepository _departmentRepository;
        private readonly AppointmentHelper _appointmentHelper;

        public MhrsService(IAvailableAppointmentRepository availableAppointmentRepository, IDepartmentRepository departmentRepository, IUserAppointmentRepository userAppointmentRepository, AppointmentHelper appointmentHelper)
        {
            _availableAppointmentRepository = availableAppointmentRepository;
            _departmentRepository = departmentRepository;
            _userAppointmentRepository = userAppointmentRepository;
            _appointmentHelper = appointmentHelper;
        }

        public CheckAvailabilityResponse CheckAvailability(CheckAvailabilityRequest request)
        {
            if (string.IsNullOrEmpty(request.Department))
                return new CheckAvailabilityResponse() { isAvailable = false };

            var availableAppointment = _appointmentHelper.GetAvailableAppointment(request.Department, request.Date, request.UserId, request.TimePreference);

            if (availableAppointment == null)
                return new CheckAvailabilityResponse() { isAvailable = false };

            var response = new CheckAvailabilityResponse();

            response.isAvailable = true;
            response.timeSlot = availableAppointment!.AppointmentDate.ToString();
            response.doctorName = availableAppointment!.Doctor!.Title + " " + availableAppointment!.Doctor!.Name;

            return response;
        }

        public BookAppointmentResponse BookAppointment(BookAppointmentRequest request)
        {
            if (string.IsNullOrEmpty(request.Department) || string.IsNullOrEmpty(request.UserId) || string.IsNullOrEmpty(request.Date))
                return new BookAppointmentResponse() { success = false };

            var availableAppointment = _appointmentHelper.GetAvailableAppointment(request.Department!, request.Date, request.UserId, request.TimePreference);

            if (availableAppointment == null)
                return new BookAppointmentResponse() { success = false };

            var result = _userAppointmentRepository.Add(new UserAppointment() { AvailableAppointment = availableAppointment, AvailableAppointmentId = availableAppointment!.Id, UserId = Guid.Parse(request.UserId!) });

            if (!result)
                return new BookAppointmentResponse() { success = false };

            return new BookAppointmentResponse() { success = true };
        }

        public CancelAppointmentResponse CancelAppointment(CancelAppointmentRequest request)
        {
            if (string.IsNullOrEmpty(request.Department) || string.IsNullOrEmpty(request.UserId) || string.IsNullOrEmpty(request.Date))
                return new CancelAppointmentResponse() { success = false };

            var department = _departmentRepository.Get(request.Department!);

            if (department == null)
                return new CancelAppointmentResponse() { success = false };

            DateTime? date = null;

            if (!string.IsNullOrEmpty(request.Date))
                date = DateTime.Parse(request.Date);

            var userAppointment = _userAppointmentRepository.Get(department!.Id, date, Guid.Parse(request.UserId!));

            if (userAppointment == null)
                return new CancelAppointmentResponse() { success = false };

            var result = _userAppointmentRepository.Remove(userAppointment!);

            if (!result)
                return new CancelAppointmentResponse() { success = false };

            return new CancelAppointmentResponse() { success = true };
        }

        public ListAppointmentResponse ListAppointment(ListAppointmentRequest request)
        {
            var response = new ListAppointmentResponse();

            DateTime? date = null;

            try
            {
                if (!string.IsNullOrEmpty(request.Date))
                    date = Convert.ToDateTime(request.Date);
            }
            catch
            {
            }

            var appointmentList = _userAppointmentRepository.GetAllDateOfRange(Guid.Parse(request.UserId!), date);

            if (appointmentList != null && appointmentList.Count > 0)
            {
                foreach (var appointment in appointmentList)
                {
                    response.Appointments.Add(new AppointmentDto()
                    {
                        Department = appointment.AvailableAppointment!.Department!.Name,
                        Doctor = appointment.AvailableAppointment!.Doctor!.Title + " " + appointment.AvailableAppointment!.Doctor!.Name,
                        Date = appointment.AvailableAppointment!.AppointmentDate.ToString()
                    });
                }
            }

            return response;
        }
    }
}
