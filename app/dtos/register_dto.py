from app import db
from app.models.user import User
from marshmallow import Schema, fields, post_load, validates, ValidationError
from werkzeug.security import generate_password_hash
import re

class RegisterDto(Schema):
    title = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    username = fields.String(required=True)
    email = fields.String(required=True) 
    password = fields.String(required=True)


    @post_load
    def make_object(self, data, **kwargs):
        data['password_hash'] = generate_password_hash(data['password'])
        del data['password']
        return User(**data)
        


    @validates('title')
    def validates_title(self, value):
        if len(value) > 10:
            raise ValidationError("Title cannot exceed 10 characters.") 
        
        if not re.match('^[a-zA-Z]+$', value):
            raise ValidationError("Title can only contain english letters.") 
        
        
        
    @validates('first_name')
    def validates_first_name(self, value):
        if len(value) < 3 or len(value) > 50:
            raise ValidationError("First name must be between 3 and 50 characters.") 
        
        if not re.match('^[a-zA-Z]+$', value):
            raise ValidationError("First name can only contain english letters.") 
        


    @validates('last_name')
    def validates_last_name(self, value):
        if len(value) < 3 or len(value) > 50:
            raise ValidationError("Last name must be between 3 and 50 characters.") 
        
        if not re.match('^[a-zA-Z]+$', value):
            raise ValidationError("Last name can only contain english letters.") 



    @validates('username')
    def validates_username(self, value):
        if len(value) < 3 or len(value) > 50:
            raise ValidationError("Username must be between 3 and 50 characters.") 
        
        if not re.match('^[a-zA-Z0-9_-]+$', value):
            raise ValidationError("Username must contain english letters, numbers and special characters (-, _).")             

        user = db.session.query(User).filter_by(username=value).one_or_none()
        if user:        
            raise ValidationError("Username is already used.")             



    @validates('password')
    def validates_password(self, value):
        if len(value) < 8:
            raise ValidationError('Password must be at least 3 characters.')
            
        pattern =  r"^(?=.*[a-zA-Z])(?=.*\d)(?=.*[_$%@-]).{8,}$"
        message = 'Password must contain at least one english letter, one digit, and one special character ($, _, %, @, -).'
        
        if not re.match(pattern, value):
            raise ValidationError(message)
        
        
        
    @validates('email')
    def validates_email(self, value):
           
        pattern =  r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
        message = 'Enter a valid email'
        
        if not re.match(pattern, value):
            raise ValidationError(message)
        
        user = db.session.query(User).filter_by(email=value).one_or_none()
        if user:        
            raise ValidationError("Email is already exist.")