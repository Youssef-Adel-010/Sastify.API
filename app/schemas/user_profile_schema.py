from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from sqlalchemy import Column
from app.models.user import User

class UserProfileSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relations = True
        load_instance = True
        exclude = ('id', 'is_deleted_user', 'password_hash', 'secret_key')