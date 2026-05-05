using MhrsWebApi.Domain;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection.Metadata;
using System.Text;
using System.Threading.Tasks;

namespace MhrsWebApi.EntityFramework
{
    public class MhrsDbContext : DbContext
    {
        public MhrsDbContext(DbContextOptions<MhrsDbContext> options) : base(options)
        {
        }

        public DbSet<UserAppointment> UserAppointments { get; set; }
        public DbSet<AvailableAppointment> AvailableAppointments { get; set; }
        public DbSet<Doctor> Doctors { get; set; }
        public DbSet<Department> Departments { get; set; }

        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {

        }
    }
}
