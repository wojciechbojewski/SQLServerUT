import unittest

import pymssql
import pyodbc

from sqlalchemy import create_engine, text, select, insert, inspect, Column, Integer, String, DateTime, MetaData
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.ext.automap import automap_base

class TestSQLServerUTpy(unittest.TestCase):

    """
    PyOdbc
    https://github.com/mkleehammer/pyodbc/    
    """
    def test_how_works_pyodbc(self):
        
        server = '192.168.100.30,1433' 
        dbname = 'SQLServerUT' 
        driver = 'ODBC Driver 17 for SQL Server'
        connstring = f'DRIVER={driver};SERVER={server};DATABASE={dbname};Trusted_Connection=yes;'
        
        with  pyodbc.connect(connstring) as cnxn:
            print(cnxn.execute("SELECT @@version;").fetchall())
            #with cnxn.cursor() as cursor:
            #    cursor.execute("SELECT @@version;") 
            #    row = cursor.fetchone() 
            #    while row: 
            #        print(row[0])
            #        row = cursor.fetchone()

            sql = """\
            SET NOCOUNT ON;
            DECLARE @rv int;
            EXEC @rv = dbo.usp_SimpleAdd ?,?;
            SELECT @rv AS return_value;
            """
            params = (2, 3)
            result = cnxn.execute(sql, params).fetchall()
            print(result)
            self.assertEqual(5, result[0][0])

        self.assertTrue(True, "Done")

    """
    PyMsSql
    https://github.com/pymssql/pymssql
    https://pymssql.readthedocs.io/en/stable/
    """
    def test_how_works_mssql(self):

        server = '192.168.100.30' 
        port = 1433
        dbname = 'SQLServerUT' 
                
        with pymssql.connect(host=server, port=port, database=dbname) as conn:
            with conn.cursor(as_dict=True) as cursor:
                cursor.execute('SELECT @@version as ver')
                for row in cursor:
                    print(f"{ row['ver'] }")
        conn.close()
        self.assertTrue(True, "Done")

    """
    SQLAlchemy
    https://www.sqlalchemy.org/
    """
    def test_how_works_sqlalchemy_1_engine(self):

        server = '192.168.100.30,1433' 
        dbname = 'SQLServerUT' 
        driver = 'ODBC Driver 17 for SQL Server'
        
        engine =  create_engine(f'mssql+pyodbc://{server}/{dbname}?driver={driver}')
        with engine.connect() as conn:
            result = conn.execute(text("select @@version as ver")).all()
            print(result)
            result = conn.execute(text("DECLARE @rc int; EXEC @rc = usp_SimpleAdd :a, :b SELECT @rc"), {"a": 2, "b":7}).all()
            print(result)
            conn.close()

        self.assertTrue(True, "Done")

    def test_how_works_sqlalchemy_2_pandas(self):

        import pandas as pd

        server = '192.168.100.30,1433' 
        dbname = 'SQLServerUT' 
        driver = 'ODBC Driver 17 for SQL Server'
        engine =  create_engine(f'mssql+pyodbc://{server}/{dbname}?driver={driver}')
        conn = engine.connect()

        stmt = text('select id, name, created from Users')
        print(stmt)
        df = pd.read_sql(stmt, conn, index_col="id")
        print(df)

        self.assertTrue(True, "Done")


    def test_how_works_sqlalchemy_3_inspect(self):

        server = '192.168.100.30,1433' 
        dbname = 'SQLServerUT' 
        driver = 'ODBC Driver 17 for SQL Server'
        engine =  create_engine(f'mssql+pyodbc://{server}/{dbname}?driver={driver}')

        info = inspect(engine);
        print(info.get_schema_names())
        print(info.get_table_names())

        self.assertTrue(True, "Done")

    def test_how_works_sqlachemy_4_sql_select_insert(self):

        server = '192.168.100.30,1433' 
        dbname = 'SQLServerUT' 
        driver = 'ODBC Driver 17 for SQL Server'
        engine =  create_engine(f'mssql+pyodbc://{server}/{dbname}?driver={driver}')

        Base = declarative_base()
        class User(Base):
            __tablename__ = "Users"
            __table_args__ = dict(schema="foo")
            id = Column(Integer, primary_key=True)
            name = Column(String(64))
            created = Column(DateTime)

        Base.metadata.create_all(engine, checkfirst=True)

        stmt = select(User).where(User.id==1).order_by(User.created)
        print(stmt)

        stmt = insert(User).values(name='test')
        print(stmt)

        self.assertTrue(True, "Done")

    def test_how_works_sqlalchemy_5_session(self):

        server = '192.168.100.30,1433' 
        dbname = 'SQLServerUT' 
        driver = 'ODBC Driver 17 for SQL Server'
        engine =  create_engine(f'mssql+pyodbc://{server}/{dbname}?driver={driver}')
        conn = engine.connect()

        with Session(conn) as session:
            print(session.execute(text("select * from Users")).all())
            session.execute(text("delete from Users where id=1"))
            print(session.execute(text("select * from Users")).all())
            session.rollback()
            print(session.execute(text("select * from Users")).all())
            session.close()

        self.assertTrue(True, "Done")

    def test_how_works_sqlalchemy_6_reflect(self):
        server = '192.168.100.30,1433' 
        dbname = 'SQLServerUT' 
        driver = 'ODBC Driver 17 for SQL Server'
        engine =  create_engine(f'mssql+pyodbc://{server}/{dbname}?driver={driver}')

        meta = MetaData(schema="foo")
        meta.reflect(engine, views=True)
        Base = automap_base(metadata=meta)
        Base.prepare(autoload_with=engine)

        User = Base.classes.Users
        tables = Base.metadata.tables
        print(tables)

        user = User(name='SQLAlchemyUser1')
        with Session(engine) as session:
            session.add(user)
            session.commit()
            print(session.execute(text("select * from foo.Users")).all())
            session.delete(user)
            session.commit()
            print(session.execute(text("select * from foo.Users")).all())
            session.close()

        self.assertTrue(True, "Done")


if __name__ == '__main__':

    unittest.main()