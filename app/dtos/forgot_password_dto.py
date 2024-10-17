from marshmallow import Schema, fields, post_load, validates, ValidationError
import re
from app import db
from app.models.user import User


class ForgotPasswordDto(Schema):
    email = fields.String(required=True)

    @post_load
    def make_object(self, data, **kwargs):
        return data['email']


    @validates('email')
    def validates_email(self, value):
           
        pattern =  r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
        
        if not re.match(pattern, value):
            raise ValidationError('Invalid email')
        
        email = db.session.query(User).filter_by(email=value).one_or_none()
        
        if not email:
            raise ValidationError('Invalid email')