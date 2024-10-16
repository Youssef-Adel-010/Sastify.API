from flask import abort
from flask_sqlalchemy import SQLAlchemy
from injector import inject
from app.dtos.register_dto import RegisterDto
from app.models.role import Role
from app.models.user import User

class UserManagementRepository:
    @inject
    def __init__(self, db: SQLAlchemy):
        self.db = db
        

    def register(self, user: User):
        role = self.db.session.query(Role).filter_by(name='user').one_or_none()
        
        if not role:
            abort(500, description={'ValidationErrors': 'The required role is not exist'})

        user.roles.append(role)
        
        self.db.session.add(user)
        self.db.session.commit()