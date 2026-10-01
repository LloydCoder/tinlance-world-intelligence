import unittest
from api.query.postgres import PostgresQueryService

class Cursor:
    def __init__(self,rows): self.rows=rows
    def execute(self,sql,args=()): self.sql=sql; self.args=args; return self
    def fetchall(self): return self.rows
    def fetchone(self): return (1,)

class Connection:
    def __init__(self): self.cursor=Cursor([({"id":"e1"},)])
    def __enter__(self): return self
    def __exit__(self,*args): return False
    def execute(self,sql,args=()): return self.cursor.execute(sql,args)
    def close(self): pass

class Pool:
    def connection(self): return Connection()

class PostgresQueryTests(unittest.TestCase):
    def test_allowlisted_resource_uses_parameterized_limits(self):
        page=PostgresQueryService(Pool()).query("entities",cursor=0,limit=1)
        self.assertEqual(page.items,[{"id":"e1"}])
        self.assertEqual(page.next_cursor,None)
    def test_unknown_resource_fails_closed(self):
        with self.assertRaises(KeyError): PostgresQueryService(Pool()).query("passwd")

if __name__=="__main__": unittest.main()
