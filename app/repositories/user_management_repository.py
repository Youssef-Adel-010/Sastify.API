from flask import abort
from flask_jwt_extended import create_access_token
from flask_sqlalchemy import SQLAlchemy
from injector import inject
import pyotp
from app.models.blocklist import Blocklist
from app.models.role import Role
from app.models.user import User
from app.models.user_token import UserToken
from werkzeug.security import check_password_hash, generate_password_hash


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
        user.secret_key = pyotp.random_base32()
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
        if user_in_db.is_2FA_enabled:
            return user_in_db
        existing_access_token = self.db.session.query(UserToken).filter_by(user_id=user_in_db.id).one_or_none()
        if existing_access_token:
            self.db.session.delete(existing_access_token)
        token = UserToken(
            user_id=user.id,
            name='access_token',
            value=create_access_token(identity=user.username)
        )
        user_in_db.tokens.append(token)
        self.db.session.commit()
        return token.value
    
    def login_with_otp(self, user: User):

        existing_access_token = self.db.session.query(UserToken).filter_by(user_id=user.id).one_or_none()
        if existing_access_token:
            self.db.session.delete(existing_access_token)
        token = UserToken(
                user_id=user.id,
                name='access_token',
                value=create_access_token(identity=user.username)
            )
        user.tokens.append(token)
        self.db.session.commit()
        return token.value
        
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
    
    def enable_2FA(self, user: User):
        user.is_2FA_enabled = True
        self.db.session.commit()
        
    def logout(self, jti):
        blocked_jti = Blocklist(jti=jti)
        self.db.session.add(blocked_jti)
        self.db.session.commit()