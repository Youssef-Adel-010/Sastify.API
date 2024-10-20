from marshmallow import post_dump
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from sqlalchemy import Column
from app.models.user import User

class AllUsersAdminSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relations = True
        load_instance = True