from app import app
from model.user_model import user_model
from flask import request
import logging
from pydantic import BaseModel
import pydantic
import string

logging.basicConfig(filename="app.log",
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

# class User(BaseModel):
#     name : str
#     email : str
#     phone: int
#     role: str
#     password : str

#     @pydantic.validator('email')
#     def email_must_contain_at(cls, value):
#         if '@' not in value:
#             raise ValueError('invalid email address')
#         return value

#     # def __repr__(self):
#     #     return self.email
    
#     @pydantic.validator('phone')
#     def phone_must_contain_at(cls, value):
#         if len(value)!=10:
#             raise ValueError('invalid number address')
#         return value

#     @pydantic.validator("password")
#     @classmethod
#     def password_validation(cls,value):
#         if len(value)<8:
#             raise ValueError("password must be atlease 8 characters long")
        
#         if any(p in value for p in string.punctuation):
#             if any(d in value for d in string.digits):
#                 if any(l in value for l in string.ascii_lowercase):
#                     if any(u in value for u in string.ascii_uppercase):
#                         return value
#         raise ValueError("Password must have atleast one punctuation,digit, upper and lower case character")

# fo_data = {
#     'name':request.form.get('name'),
#     'email':request.form.get('email'),
#     'phone':request.form.get('phone'),
#     'role':request.form.get('role'),
#     'password':request.form.get('password')
# }

# my_data = User(**fo_data)
# print(my_data)

obj = user_model()

@app.route('/user/getall')
def user_getall_controller():
    return obj.user_getall_model()

@app.route('/user/addone',methods=['POST'])
def user_addone_controller():
    try:
        if len(request.form)<5:
             raise Exception("fill all required field")
        else:
            # print("form",request.form.get('name'))
            # user = User(**request.form)
            return obj.user_addone_model(request.form)
    except Exception as e:
        logging.error(e,exc_info=True)

@app.route('/user/update',methods=['PUT'])
def user_update_controller():
    return obj.user_update_model(request.form)

@app.route('/user/delete/<id>',methods=['DELETE'])
def user_delete_controller(id):
    return obj.user_delete_model(id)

@app.route('/user/patch/<id>',methods=['PATCH'])
def user_patch_controller(id):
    return obj.user_patch_model(request.form,id)