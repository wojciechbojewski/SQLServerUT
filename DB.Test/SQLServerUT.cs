using System.Data;
using System.Data.SqlClient;

namespace DB.Test
{
    public class SQLServerUT : IDisposable
    {

        SqlConnection conn;

        public SQLServerUT()
        {
            conn = new SqlConnection("Data Source=192.168.100.30,1433;Initial Catalog=SQLServerUT;Integrated Security=SSPI;");
            conn.Open();
        }

        public void Dispose()
        {
            conn.Dispose();
        }


        [Theory]
        [InlineData(2, 3, 5)]
        [InlineData(-5, 5, 0)]
        [InlineData(-2, -5, -7)]
        public void usf_SimpleAdd_IntegerValues_Calculated(int a, int b, int expected)
        {

            if (conn != null && conn.State == ConnectionState.Open)
            {
                string sql = "SELECT dbo.usf_SimplyAdd(@a, @b);";
                SqlCommand cmd = new SqlCommand(sql, conn);

                cmd.Parameters.Add("@a", SqlDbType.Int);
                cmd.Parameters["@a"].Value = a;

                cmd.Parameters.Add("@b", SqlDbType.Int);
                cmd.Parameters["@b"].Value = b;

                Int32 result = (Int32)cmd.ExecuteScalar();

                Assert.Equal(expected, result);
            }


        }

        [Theory]
        [InlineData(2, 3, 5)]
        [InlineData(-5, 5, 0)]
        [InlineData(-2, -5, -7)]
        public void usp_SimpleAdd_IntegerValues_Calculated(int a, int b, int expected)
        {

            if (conn != null && conn.State == ConnectionState.Open)
            {

                SqlCommand cmd = new SqlCommand("dbo.usp_SimpleAdd", conn);
                cmd.CommandType = CommandType.StoredProcedure;

                SqlParameter rc = cmd.Parameters.Add("@Return Value", SqlDbType.Int);
                rc.Direction = ParameterDirection.ReturnValue;

                cmd.Parameters.Add("@a", SqlDbType.Int).Value = a;
                cmd.Parameters.Add("@b", SqlDbType.Int).Value = b;

                int rows = cmd.ExecuteNonQuery();
                int result = (int)cmd.Parameters["@Return Value"].Value;

                Assert.Equal(expected, result);
            
            }

        }

        [Fact]
        public void usp_ShowLogs_HappyPath_ShowLoginsOnly()
        {


            if (conn != null && conn.State == ConnectionState.Open)
            {

                SqlCommand cmd = new SqlCommand("TRUNCATE TABLE Users; TRUNCATE TABLE Events; TRUNCATE TABLE Logs", conn);
                cmd.ExecuteNonQuery();

                cmd = new SqlCommand("INSERT INTO Users (name) VALUES ('TestUser1'), ('TestUser2'), ('TestUser3'); INSERT INTO Events (name, type) VALUES ('Login',1), ('Logout',1);  INSERT INTO Logs (user_id, event_id) VALUES (2, 1), (2,2);", conn);
                cmd.ExecuteNonQuery();

                cmd = new SqlCommand("dbo.usp_ShowLogs", conn);
                cmd.CommandType = CommandType.StoredProcedure;
                cmd.Parameters.Add("@event_type", SqlDbType.Int).Value = 1; //Login only!

                using (SqlDataReader reader = cmd.ExecuteReader())
                {
                    while (reader.HasRows)
                    {
                        while (reader.Read())
                        {
                            string user_name = reader.GetString(1);
                            string event_name = reader.GetString(2);

                            Assert.Equal("Login", event_name);
                            Assert.Equal("TestUser2", user_name);

                        }
                        reader.NextResult();
                    }

                }
            }

        }


    }
}