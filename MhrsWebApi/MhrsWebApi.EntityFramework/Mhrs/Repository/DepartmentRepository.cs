using MhrsWebApi.Domain;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MhrsWebApi.EntityFramework
{
    public class DepartmentRepository : IDepartmentRepository
    {
        private readonly MhrsDbContext _context;

        public DepartmentRepository(MhrsDbContext context)
        {
            _context = context;
        }

        public Department? Get(string department)
        {
            return _context.Departments
                           .FirstOrDefault(w => w.Name.Contains(department));
        }
    }
}
