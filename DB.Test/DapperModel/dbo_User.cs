using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DB.Test.DapperModel
{
    public class dbo_User
    {
        public int? Id { get; set; }
        public String name { get; set; }
        public DateTime? created { get; set; } 

    }
}
