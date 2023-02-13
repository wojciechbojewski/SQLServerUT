using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DB.Test.DapperModel
{
    public class dbo_Event
    {
        public int? id { get; set; }
        public string name { get; set; }
        public DateTime? created { get; set; }
    }
}
