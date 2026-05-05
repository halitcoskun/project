using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MhrsWebApi.Application
{
    public class CheckAvailabilityResponse
    {
        public bool isAvailable { get; set; }
        public string doctorName { get; set; }
        public string timeSlot { get; set; }
    }
}
