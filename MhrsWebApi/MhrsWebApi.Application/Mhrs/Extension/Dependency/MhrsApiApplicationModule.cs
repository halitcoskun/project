using MhrsWebApi.Application;

namespace Microsoft.Extensions.DependencyInjection
{
    public static class MhrsApiApplicationModule
    {
        public static IServiceCollection AddApplicationServices(this IServiceCollection services)
        {
            services.AddScoped<AppointmentHelper>();

            // Mhrs servisimiz için DI tanımı
            services.AddScoped<IMhrsService, MhrsService>();
            return services;
        }
    }
}
