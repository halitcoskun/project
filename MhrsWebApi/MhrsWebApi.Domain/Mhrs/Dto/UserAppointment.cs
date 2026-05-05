using System.ComponentModel.DataAnnotations.Schema;

namespace MhrsWebApi.Domain
{
    [Table("UserAppointment")]
    public class UserAppointment : AggregateRoot
    {
        public Guid UserId { get; set; }
        public int AvailableAppointmentId { get; set; }
        public AvailableAppointment? AvailableAppointment { get; set; }
    }
}
