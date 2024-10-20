from marshmallow import Schema, fields, post_load, validates, ValidationError, validates_schema
import re
from app import db
from app.models.user import User


class ResetPasswordDto(Schema):
    new_password = fields.String(required=True)
    confirm_password = fields.String(required=True)

    @post_load
    def make_object(self, data, **kwargs):
        data['new_password'] = str(data['new_password']).strip()
        return {'new_password': data['new_password']}

    @validates('new_password')
    def validates_password(self, value):
        if len(value) < 8:
            raise ValidationError('Password must be at least 3 characters.')
        pattern =  r"^(?=.*[a-zA-Z])(?=.*\d)(?=.*[_$%@-]).{8,}$"
        message = 'Password must contain at least one english letter, one digit, and one special character ($, _, %, @, -).'
        if not re.match(pattern, value):
            raise ValidationError(message)
        
    @staticmethod
    def validate_confirm_passwords(data):
        if data['new_password'] != data['confirm_password']:
            raise ValidationError(field_name="confirm_password", message="Confirm password doesn't match the entered password.")

    @validates_schema
    def validate_schema(self, data, **kwargs):
        self.validate_confirm_passwords(data)