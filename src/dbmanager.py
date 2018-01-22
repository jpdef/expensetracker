import sqlite3
from env import DATABASEPATH

class DBManager:
     
    def __init__(self,tablename, columns):
        #Connect to database
        self.tablename = tablename
        self.columns = columns
        self.con = sqlite3.connect(DATABASEPATH)
        self.cur = self.con.cursor()
        
        #Construct query strings
        self.create_str = "CREATE TABLE %s ("+ ', '.join([ '%s' for x in range(len(columns))])  + ")"
        self.insert_str = "INSERT INTO " + tablename + " VALUES ("+ ",".join([ "?" for x in range(len(columns))])  + ")"
        self.get_str    = "SELECT * FROM " + tablename + " WHERE %s=?"
        self.get_all_str= "SELECT * FROM " + tablename
        #update_str = "UPDATE" + table_name + " ? 
        
        #If table exists use previous table if not create new one
        try:
            self.cur.execute('SELECT * FROM '  + tablename)
        except sqlite3.Error as E:
            self.create_table(tablename,columns)
       
    def __del__(self):
        self.con.commit()
        self.con.close()

   
    def create_table(self,tablename,columns):
        print(self.create_str)
        cmdstr =  self.create_str % tuple([tablename] + columns ) 
        self.cur.execute(cmdstr)

    def load(self,data):
        pass
    
    def load_spreadsheet(self):
        pass

    def insert(self,args):
        try:
            self.cur.execute(self.insert_str, tuple(args))
        except sqlite3.Error as E:
            print("DBManager insert sqlite error:" + str(E))

    def update(self):
        pass

    def delete(self):
        pass

    def get_all(self):
        try:
            self.cur.execute(self.get_all_str)
            data =  self.cur.fetchall()
            return ( [ dict(zip(self.columns,d)) for d in data] )
        except sqlite3.Error as E:
            print("DBManager get sqlite error:" + str(E))
            return []


    def get(self,key,value):
        try:
            query = self.get_str % key
            print(query)
            self.cur.execute(query, (value,))
            return self.cur.fetchone()
        except sqlite3.Error as E:
            print("DBManager get sqlite error:" + str(E))
        

if __name__ == "__main__":
    #Do the tests
    dbman = DBManager("transactions", ["date text", "category text","desc text"])
    #dbman.insert(["2017-1-10","food","in-in-out"])
    #dbman.insert(["2017-1-10","trans","oil"])
    #dbman.insert(["2017-1-10","watch","expense"])
    dbman.insert(["2017-1-10","PGE","utilities"])
    print(dbman.get("category","food"))
    print(dbman.get_all())

