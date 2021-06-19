import psycopg2
from constants import queries


class Database():

    def __init__(self, db_url:str):

        self.conn =  psycopg2.connect(db_url)

    def __del__(self):

        self.conn.close()  

    def add_user(self,user_id):

        cur = self.conn.cursor()
        cur.execute(queries.ADD_USER,{"id":user_id})
        self.conn.commit()
        cur.close()   

    def add_entry(self,table,user_id,val):

        cur = self.conn.cursor()
        
        if table ==1:
            cur.execute(queries.ADD_DISTRICT,{"user_id":user_id,"district_id":val})
        elif table ==2:
            cur.execute(queries.ADD_PINCODE,{"user_id":user_id,"pincode":val})    

        self.conn.commit()
        cur.close()   

    def get_entries_count(self,id):    

        cur = self.conn.cursor()   
        cur.execute(queries.GET_ENTRIES_COUNT,{"id":id})
        count = cur.fetchone()
        cur.close()  
        return count

    def get_pref_for_user(self,id):
        cur = self.conn.cursor()   
        cur.execute(queries.GET_PREFERENCE,{"id":id})
        pref = cur.fetchone()
        cur.close()  
        return pref

    def set_preference(self,pref,id):

        cur = self.conn.cursor()
        cur.execute(queries.SET_PREFERENCE,{"age":pref["age"],"dose":pref["dose"],"vaccine":pref["vaccine"],"fee":pref["fee"],"interval":pref["interval"],"id":id})
        self.conn.commit()
        cur.close()  

    def get_districts(self):  

        cur = self.conn.cursor()
        cur.execute(queries.GET_DISTRICTS)
        districts = cur.fetchall()
        cur.close() 
        return districts

    def get_pincodes(self):  

        cur = self.conn.cursor()
        cur.execute(queries.GET_PINCODES)
        pincodes = cur.fetchall()
        cur.close() 
        return pincodes

    def get_users(self): 

        cur = self.conn.cursor()
        cur.execute(queries.GET_USERS)
        users = cur.fetchall()
        cur.close() 
        return users 

    def get_districts_for_user(self,id): 

        cur = self.conn.cursor()
        cur.execute(queries.GET_DISTRICTS_FOR_USER,{"id":id})
        districts = cur.fetchall()
        cur.close() 
        return districts    

    def get_pincodes_for_user(self,id): 

        cur = self.conn.cursor()
        cur.execute(queries.GET_PINCODES_FOR_USER,{"id":id})
        pincodes = cur.fetchall()
        return pincodes 

    def get_last_msg_id(self,id):
        cur = self.conn.cursor()
        cur.execute(queries.GET_LAST_MSG_ID,{"id":id})
        msg_id = cur.fetchone()
        cur.close()  
        return msg_id  

    def update_last_sent(self,id,time,msg_id):

        cur = self.conn.cursor()
        cur.execute(queries.UPDATE_LAST_SENT,{"id":id,"time":time,"msg_id":msg_id})
        self.conn.commit()
        cur.close()   

    def remove_district(self,id,district):  

        cur = self.conn.cursor()
        cur.execute(queries.REMOVE_DISTRICT,{"id":id,"district_id":district})
        self.conn.commit()
        cur.close() 

    def remove_pincode(self,id,pincode):  

        cur = self.conn.cursor()
        cur.execute(queries.REMOVE_PINCODE,{"id":id,"pincode":pincode})
        self.conn.commit()
        cur.close()       
        
