using System.ComponentModel.DataAnnotations.Schema;

namespace MhrsWebApi.Domain
{
    [Table("Doctor")]
    public class Doctor : AggregateRoot
    {
        public string Title { get; set; } = "";
        public string Name { get; set; } = "";
        public int DepartmentId { get; set; }
        public Department? Department { get; set; }
        public ICollection<AvailableAppointment> AvailableAppointments { get; set; } = new List<AvailableAppointment>();
    }
}
