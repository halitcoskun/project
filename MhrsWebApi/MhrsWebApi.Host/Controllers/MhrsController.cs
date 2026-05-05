using MhrsWebApi.Application;
using Microsoft.AspNetCore.Mvc;

namespace MhrsWebApi.Host.Controllers
{
    [ApiController]
    [Route("api/[controller]/[action]")]
    public class MhrsController : ControllerBase
    {
        private readonly ILogger<MhrsController> _logger;
        private readonly IMhrsService _mhrsService;

        public MhrsController(ILogger<MhrsController> logger, IMhrsService mhrsService)
        {
            _logger = logger;
            _mhrsService = mhrsService;
        }

        [HttpPost]
        public CheckAvailabilityResponse CheckAvailability(CheckAvailabilityRequest request)
        {
            return _mhrsService.CheckAvailability(request);
        }

        [HttpPost]
        public BookAppointmentResponse BookAppointment(BookAppointmentRequest request)
        {
            return _mhrsService.BookAppointment(request);
        }

        [HttpPost]
        public CancelAppointmentResponse CancelAppointment(CancelAppointmentRequest request)
        {
            return _mhrsService.CancelAppointment(request);
        }

        [HttpPost]
        public ListAppointmentResponse ListAppointment(ListAppointmentRequest request)
        {
            return _mhrsService.ListAppointment(request);
        }
    }
}
