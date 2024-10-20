from marshmallow import Schema, fields, post_load, validates, ValidationError
import re
from app import db
from app.models.user import User


class ForgotPasswordDto(Schema):
    email = fields.String(required=True)

    @post_load
    def make_object(self, data, **kwargs):
        data['email'] = str(data['email']).strip()
        return data['email']

    @validates('email')
    def validates_email(self, value):
        pattern =  r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, value):
            raise ValidationError('Invalid email')