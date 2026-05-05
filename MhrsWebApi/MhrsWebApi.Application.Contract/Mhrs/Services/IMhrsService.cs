using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MhrsWebApi.Application
{
    public interface IMhrsService
    {
        public CheckAvailabilityResponse CheckAvailability(CheckAvailabilityRequest request);

        public BookAppointmentResponse BookAppointment(BookAppointmentRequest request);

        public CancelAppointmentResponse CancelAppointment(CancelAppointmentRequest request);

        public ListAppointmentResponse ListAppointment(ListAppointmentRequest request);
    }
}
