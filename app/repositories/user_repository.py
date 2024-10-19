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

class UserRepository:
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
        try:
            self.db.session.commit()
        except Exception as ex:
            self.db.session.rollback()
            abort(500, description=ex)
            
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
        try:
            self.db.session.commit()
        except Exception as ex:
            self.db.session.rollback()
            abort(500, description=ex)
        return token.value
        
    def logout(self, jti):
        blocked_jti = Blocklist(jti=jti)
        self.db.session.add(blocked_jti)
        try:
            self.db.session.commit()
        except Exception as ex:
            self.db.session.rollback()
            abort(500, description=ex)
        
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
        try:
            self.db.session.commit()
        except Exception as ex:
            self.db.session.rollback()
            abort(500, description=ex)
        return token.value

    def update_user_data(self, user: User, updated_user: User):
        if updated_user.title is not None and updated_user.title != user.title:
            user.title = updated_user.title
        if updated_user.first_name is not None and updated_user.first_name != user.first_name:
            user.first_name = updated_user.first_name
        if updated_user.last_name is not None and updated_user.last_name != user.last_name:
            user.last_name = updated_user.last_name
        if updated_user.email is not None and updated_user.email != user.email:
            user.email = updated_user.email
        try:
            self.db.session.commit()
        except Exception as ex:
            self.db.session.rollback()
            abort(500, description=ex)
        return user

    def reset_password(self, user: User, new_password):
        user.password_hash = generate_password_hash(new_password)
        try:
            self.db.session.commit()
        except Exception as ex:
            self.db.session.rollback()
            abort(500, description=ex)        

    def change_password(self, user: User, new_password):
        user.password_hash = generate_password_hash(new_password)
        try:
            self.db.session.commit()
        except Exception as ex:
            self.db.session.rollback()
            abort(500, description=ex)        

    def enable_2FA(self, user: User):
        user.is_2FA_enabled = True
        try:
            self.db.session.commit()
        except Exception as ex:
            self.db.session.rollback()
            abort(500, description=ex)
        
    def disable_2FA(self, user: User):
        user.is_2FA_enabled = False
        try:
            self.db.session.commit()
        except Exception as ex:
            self.db.session.rollback()
            abort(500, description=ex)
        
    def activate_account(self, user):
        user.is_activated_account = True
        try:
            self.db.session.commit()
        except Exception as ex:
            self.db.session.rollback()
            abort(500, description=ex)
        
        
    def get_user_by_username(self, username):
        user = self.db.session.query(User).filter_by(username=username).one_or_none()
        return user
        
    def get_user_by_email(self, email):
        user = self.db.session.query(User).filter_by(email=email).one_or_none()
        return user
    
    def verify_password(self, real_password, entered_password):
        return check_password_hash(real_password, entered_password)