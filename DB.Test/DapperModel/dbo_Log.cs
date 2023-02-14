using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DB.Test.DapperModel
{
    public class dbo_Log
    {
        public int? id { get; set; }
        public int user_id { get; set; }
        public int event_id { get; set; }
        public DateTime created { get; set; }
    }
}
