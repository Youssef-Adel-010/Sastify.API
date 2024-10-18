from marshmallow import Schema, fields, post_load, validates, ValidationError
import re
from app import db
from app.models.user import User


class LoginDto(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

    @post_load
    def make_object(self, data, **kwargs):
        data['password_hash'] = data['password']
        del data['password']
        return User(**data)
    
    @validates('username')
    def validates_username(self, value):
        if len(value) < 3 or len(value) > 50 or not re.match('^[a-zA-Z0-9_-]+$', value):
            raise ValidationError("Invalid credentials")

    @validates('password')
    def validates_password(self, value):
        pattern =  r"^(?=.*[a-zA-Z])(?=.*\d)(?=.*[_$%@-]).{8,}$"
        if len(value) < 8 or not re.match(pattern, value):
            raise ValidationError('Invalid credentials')
        
    