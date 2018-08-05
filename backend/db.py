import sqlite3 as sql

CREATE_URL_TABLE_QUERY = """CREATE TABLE table_url(id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                         url VARCHAR(200),
                                         key VARCHAR(1000))"""

INSERT_URL_QUERY = "INSERT INTO table_url(url, key) values (?, ?);"
FETCH_ALL_URL = "SELECT * FROM table_url"
FETCH_URL_BY_ID = "SELECT * FROM table_url WHERE id='{}'"
DELETE_URL_BY_ID = "DELETE FROM table_url WHERE id='{}'"
SEARCH_URL = "SELECT * FROM table_url WHERE key='{}'"
DROP_TABLE_URL = "DROP TABLE IF EXISTS table_url"


class DatabaseHandler:

   def __init__(self, db_name: str) -> None:
      self.db_name = db_name 
      self.con = sql.connect(self.db_name)
      self.cur = self.con.cursor()
   
   def init(self) -> None:
      self.cur.execute(CREATE_URL_TABLE_QUERY)
      self.con.commit()   
  
 
   def drop_tables(self) -> None:
      self.cur.execute(DROP_TABLE_URL)
  
 
   def add(self, **kwargs) -> None:
      self.cur.execute(INSERT_URL_QUERY, (kwargs['url'], kwargs['key']))
      self.con.commit()


   def fetch_urls(self):
      return self.cur.execute(FETCH_ALL_URL)


   def fetch_url_by_id(self, user_id: int):
      return self.cur.execute(FETCH_URL_BY_ID.format(user_id))

   
   def fetch_all_post(self):
      return self.cur.execute(FETCH_POST) 


   def search_url(self, query: str): 
      return self.cur.execute(SEARCH_URL.format(query))
      
   
   def delete_url(self, post_id: int) -> None:
      self.cur.execute(DELETE_URL_BY_ID.format(post_id))
      self.con.commit()
   

def test():
   db = DatabaseHandler('blog.db')
   db.drop_tables() 
   db.init()
   db.add(url='http://google.com', key='google123')
   
   post_all = db.fetch_url()

   for post in post_all:
      print(post)

   post_by_id = db.fetch_post_by_id(1)
   print(post_by_id.fetchone())


if __name__ == "__main__":
   test() 