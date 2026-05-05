using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MhrsWebApi.Application
{
    public class BookAppointmentRequest
    {
        public string? UserId { get; set; }
        public string Department { get; set; }
        public string Date { get; set; }
        public string? TimePreference { get; set; }
    }
}
