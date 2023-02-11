import sqlite3
import pandas as pd

class database:
    
    def __init__(self, db_name, table_name, df_results):
        
        self.db_name = db_name
        self.table_name = table_name
        self.df_results = df_results
        self.conn = sqlite3.connect('{}.db'.format(db_name))
        
        print("Successfully connected to database {}".format(db_name))
        
    def create_table(self, table_name):
        """
        function to create table (if not already present in the database)
        """
        
        query = '''Create table if not exists {} (ID INTEGER PRIMARY KEY AUTOINCREMENT,
            ROLE CHAR(200),
            COMPANY CHAR(200),
            URL CHAR(200));'''.format(table_name)        
        
        self.conn.execute(query)
        
    
    def populate_table(self, table_name, df_results):
        """
        function for adding entries to the table in the database
        """
        
        query= '''Insert into {} 
        (ROLE,COMPANY,URL) values (?,?,?)'''.format(table_name)
        
        self.conn.executemany(query, df_results.to_records(index=False))
        self.conn.commit()
        
        
    def main(self):
        """
        main function to run for storing scraped data into database
        """
        
        self.create_table(self.table_name)
        self.populate_table(self.table_name, self.df_results)
        self.conn.close()
        
        
    def check_and_reconnect(self):
        """
        helper function for re-establishing connection if database is closed
        """
        
        try:
            self.conn.cursor()
            return
        except Exception as ex:
            self.conn = sqlite3.connect('{}.db'.format(self.db_name))
            return 
        
        
    def read_from_db(self):
        """
        load data stored in database into pandas dataframe
        """
        
        self.check_and_reconnect()
        df = pd.read_sql_query("SELECT * FROM {};".format(self.table_name), db.conn)
        self.conn.close()
        return df
        
    
        