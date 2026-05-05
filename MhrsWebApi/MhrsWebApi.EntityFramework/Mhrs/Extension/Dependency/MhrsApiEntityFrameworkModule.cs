using MhrsWebApi.Domain;
using MhrsWebApi.EntityFramework;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;

namespace Microsoft.Extensions.DependencyInjection
{
    public static class MhrsApiEntityFrameworkModule
    {
        public static IServiceCollection AddDataServices(this IServiceCollection services, IConfiguration configuration)
        {
            // Mhrs servisimiz için DI tanımı
            services.AddDbContext<MhrsDbContext>(options => options.UseSqlServer(configuration.GetConnectionString("DefaultConnection")));

            services.AddScoped<IUserAppointmentRepository, UserAppointmentRepository>();
            services.AddScoped<IAvailableAppointmentRepository, AvailableAppointmentRepository>();
            services.AddScoped<IDepartmentRepository, DepartmentRepository>();

            return services;
        }
    }
}
