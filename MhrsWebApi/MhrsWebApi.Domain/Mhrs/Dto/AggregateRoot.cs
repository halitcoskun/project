using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MhrsWebApi.Domain
{
    public abstract class AggregateRoot
    {
        public int Id { get; set; }
        public DateTime SystemDate { get; set; } = DateTime.Now;
    }
}
