from flask_jwt_extended import current_user
from app import db
from app.models.user import User
from marshmallow import Schema, fields, post_load, validates, ValidationError
from werkzeug.security import generate_password_hash
import re

class UpdateDto(Schema):
    title = fields.String(required=False)
    first_name = fields.String(required=False)
    last_name = fields.String(required=False)
    email = fields.String(required=False) 

    @post_load
    def make_object(self, data, **kwargs):
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

    @validates('email')
    def validates_email(self, value):
        pattern =  r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
        message = 'Enter a valid email'
        if not re.match(pattern, value):
            raise ValidationError(message)
        user = db.session.query(User).filter_by(email=value).one_or_none()

        if user and user != current_user:        
            raise ValidationError("Email is already exist.")