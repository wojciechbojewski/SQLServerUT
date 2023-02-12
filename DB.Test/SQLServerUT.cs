using System.Data;
using System.Data.SqlClient;

namespace DB.Test
{
    public class SQLServerUT
    {
        [Theory]
        [InlineData(2, 3, 5)]
        [InlineData(-5, 5, 0)]
        [InlineData(-2, -5, -7)]
        public void usf_SimpleAdd_IntegerValues_Calculated(int a, int b, int expected)
        {
            using (SqlConnection conn = new SqlConnection("Data Source=192.168.100.30,1433;Initial Catalog=SQLServerUT;Integrated Security=SSPI;"))
            {
                string sql = "SELECT dbo.usf_SimplyAdd(@a, @b);"; 
                SqlCommand cmd = new SqlCommand(sql, conn);

                cmd.Parameters.Add("@a", SqlDbType.Int);
                cmd.Parameters["@a"].Value = a;

                cmd.Parameters.Add("@b", SqlDbType.Int);
                cmd.Parameters["@b"].Value = b;

                conn.Open();
                Int32 result = (Int32)cmd.ExecuteScalar();

                Assert.Equal(expected, result);

            }

        }
    }
}