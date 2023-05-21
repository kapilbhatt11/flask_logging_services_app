import mysql.connector
import json
from flask import make_response
import logging
from datetime import datetime,date
import time


logging.basicConfig(filename="app.log",
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

class user_model():
    def __init__(self):
        try:
            self.con = mysql.connector.connect(host='localhost',user='root',password = 'Bosch123!',database = 'flask_new_task')
            self.con.autocommit = True
            self.cur = self.con.cursor(dictionary=True)
            logging.info('connection successful')
        except:
            logging.debug("some error",exc_info=True)

    #function for viewing all user in DB 
    def user_getall_model(self):
        #connection establishment code
        self.current_time = time.time()
        self.log_date = datetime.now()

        try:
            self.cur.execute('SELECT * FROM users')
            result = self.cur.fetchall()
            if len(result)>0:
                # return json.dumps(result)
                res = make_response({"payload":result},200)
                res.headers['Access-Control-Allow-Origin']='*'
                return res
            else:
                return make_response({'massege':'No Data Found'},204)
        except:
            logging.error("something bad with user_getall_model function ",exc_info=True)

        finally:
            end = time.time() - self.current_time
            self.cur.execute(f"INSERT INTO record(function_name,execution_time,log_date,action_perform) VALUES('user_getall_model','{end}','{self.log_date}','viewing the data')")
    

    #function for adding new user in DB
    def user_addone_model(self,data):
        self.current_time = time.time()
        self.log_date = datetime.now()
        
        self.cur.execute(f"SELECT * FROM users WHERE name='{data['name']}' AND email='{data['email']}'")
        result = self.cur.fetchall()
        
        if result != []:
                return make_response({'massege':'user is already exist'},202)
        else:
            self.request_body = {
                                    'name':data['name'],
                                    'email':data['email'],
                                    'phone' : data['phone'],
                                    'role' : data['role'],
                                    'password':data['password']
                                }

            req = json.dumps(self.request_body)
            try:
                self.cur.execute(f"INSERT INTO users(name,email,phone,role,password) VALUES('{data['name']}','{data['email']}','{data['phone']}','{data['role']}','{data['password']}')")
                return make_response({'massege':'user created successfully'},201)
            
            except:
                logging.error("something bad with user_addone_model function ",exc_info=True)

            finally:
                end = time.time() - self.current_time
                self.cur.execute(f"INSERT INTO record(function_name,execution_time,log_date,action_perform,request_body) VALUES('user_addone_model','{end}','{self.log_date}','creating new user','{req}')")


    #function for updating whole data of user on the basis of ID  
    def user_update_model(self,data):
        self.current_time = time.time()
        self.log_date = datetime.now()

        #tesing inner function execting time
        store_time = {}
        def test():
            a = 15
            b = 45
            
            def sum_(x,y):
                return x+y
            st = time.time()
            s = sum_(a,b)
            et = time.time()-st
            return s,et,test.__name__
        
        inner_start1 = time.time()
        new,t = test()
        end_time = time.time()-inner_start1

        

        self.request_body = {
                                'name':data['name'],
                                'email':data['email'],
                                'phone' : data['phone'],
                                'role' : data['role'],
                                'password':data['password']
                            }
        req = json.dumps(self.request_body)

        try:
            self.cur.execute(f"UPDATE users set name='{data['name']}',email='{data['email']}',phone='{data['phone']}',role='{data['role']}',password='{data['password']}' WHERE id={data['id']} ")

            if self.cur.rowcount > 0:
                return make_response({'massege':'user updated successfully'},201)
            else:
                return make_response({'massege':'Nothing to Update'},202)
        except:
            logging.error("something bad with user_update_model function ",exc_info=True) 
        finally:
            end = time.time() - self.current_time
            self.cur.execute(f"INSERT INTO record(function_name,execution_time,log_date,action_perform,request_body,inner_function,inner_function_execution_time) VALUES('user_update_model','{end}','{self.log_date}','complete data is updating id {data['id']} user','{req}','test','{end_time}')")


    #deleting exiting users with id 
    def user_delete_model(self,id):
        self.current_time = time.time()
        self.log_date = datetime.now()

        self.cur.execute(f"SELECT * FROM  users WHERE id={id}")
        result = self.cur.fetchall()

        if result == []:
            return make_response({'massege':'Nothing to Deleted'},202)
        else:
          req = json.dumps(result[0])

        try:
            self.cur.execute(f"DELETE FROM users WHERE id={id}")
            if self.cur.rowcount > 0:
                return make_response({'massege':'user Deleted successfully'},200)
            else:
                return make_response({'massege':'Nothing to Deleted'},202)
        except:
            logging.error("something bad with user_delete_model function ",exc_info=True)
        finally:
            end = time.time() - self.current_time
            self.cur.execute(f"INSERT INTO record(function_name,execution_time,log_date,action_perform,request_body) VALUES('user_delete_model','{end}','{self.log_date}','deleting id {id} user','{req}')")

    
    #updating some data of exiting users
    def user_patch_model(self,data,id):
        self.current_time = time.time()
        self.log_date = datetime.now()
        
        self.request_body = {}
        for key in data:
            self.request_body[key]=data[key]

        req = json.dumps(self.request_body)

        try:
            qry = "UPDATE users SET "
            # print(data)
            for key in data:
                qry = qry + f"{key}='{data[key]}',"
            qry = qry[:-1] + f' WHERE id={id}'
            # # UPDATE users SET col=val, col=val, WHERE id={id}
            self.cur.execute(qry)
            if self.cur.rowcount > 0:
                return make_response({'massege':'user updated successfully'},201)
            else:
                return make_response({'massege':'Nothing to Update'},202)
        except:
            logging.error("something bad with user_patch_model function ",exc_info=True)

        finally:
            end = time.time() - self.current_time
            self.cur.execute(f"INSERT INTO record(function_name,execution_time,log_date,action_perform,request_body) VALUES('user_delete_model','{end}','{self.log_date}','deleting id {id} user','{req}')")






