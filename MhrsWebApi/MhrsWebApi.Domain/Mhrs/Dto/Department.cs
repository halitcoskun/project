using System.ComponentModel.DataAnnotations.Schema;

namespace MhrsWebApi.Domain
{
    [Table("Department")]
    public class Department : AggregateRoot
    {
        public string Name { get; set; } = "";
        public ICollection<Doctor> Doctors { get; set; } = new List<Doctor>();
        public ICollection<AvailableAppointment> AvailableAppointments { get; set; } = new List<AvailableAppointment>();
    }
}
