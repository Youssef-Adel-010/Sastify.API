from datetime import timedelta
from flask import abort
from flask_sqlalchemy import SQLAlchemy
from injector import inject
from app.dtos.register_dto import RegisterDto
from app.models.role import Role
from app.models.user import User
from app.models.user_token import UserToken
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token

class UserManagementRepository:
    @inject
    def __init__(self, db: SQLAlchemy):
        self.db = db
        


    def register(self, user: User):
        role = self.db.session.query(Role).filter_by(name='user').one_or_none()
        
        if not role:
            abort(404, description='The required role is not exist')
            return

        user.roles.append(role)
        
        self.db.session.add(user)
        self.db.session.commit()



    def login(self, user: User):
        user_in_db = self.get_user_by_username(user.username)
        
        if not user_in_db:
            abort(401, description='Invalid credentials')
            return
        
        if not self.verify_password(user_in_db.password_hash, user.password_hash):
            abort(401, description='Invalid credentials' )
            return

        existing_access_token = self.db.session.query(UserToken).filter_by(user_id=user_in_db.id).one_or_none()
        if existing_access_token:
            self.db.session.delete(existing_access_token)
        
        
        token = UserToken(
            user_id=user_in_db.id,
            name='access_token',
            value=create_access_token(identity=user_in_db.username, expires_delta=timedelta(days=30))
        )
        user_in_db.tokens.append(token)

        self.db.session.commit()
    
    
    def reset_password(self, user: User, new_password):
        user.password_hash = generate_password_hash(new_password)
        self.db.session.commit() 

        
    def get_user_by_username(self, username):
        user = self.db.session.query(User).filter_by(username=username).one_or_none()
        return user
    
        
    def get_user_by_email(self, email):
        user = self.db.session.query(User).filter_by(email=email).one_or_none()
        return user
    
    
    def verify_password(self, real_password, entered_password):
        return check_password_hash(real_password, entered_password)
    