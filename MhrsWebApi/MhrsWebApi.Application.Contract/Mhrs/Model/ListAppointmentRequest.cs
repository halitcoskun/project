using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MhrsWebApi.Application
{

    public class ListAppointmentRequest
    {
        public string UserId { get; set; }
        public string? Date { get; set; }
    }
}
