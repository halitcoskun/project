using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MhrsWebApi.Application
{
    public class ListAppointmentResponse
    {
        public List<AppointmentDto> Appointments { get; set; } = new List<AppointmentDto>();
    }
}
