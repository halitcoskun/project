using System.ComponentModel.DataAnnotations.Schema;

namespace MhrsWebApi.Domain
{
    [Table("AvailableAppointment")]
    public class AvailableAppointment: AggregateRoot
    {
        public DateTime AppointmentDate { get; set; }
        public int DepartmentId { get; set; }
        public int DoctorId { get; set; }
        public Department? Department { get; set; }
        public Doctor? Doctor { get; set; }
    }
}
