import pyotp
from flask import abort
from flask_jwt_extended import decode_token
from flask_sqlalchemy import SQLAlchemy
from injector import inject
from sqlalchemy import desc
from app.models.blocklist import Blocklist
from app.models.role import Role
from app.models.user import User
from app.models.user_token import UserToken


class AdminRepository:
    @inject
    def __init__(self, db: SQLAlchemy):
        self.db = db
                
    def get_all_users(self):
        users = self.db.session.query(User).all()
        return users
    
    def get_user(self, identifier):
        if str(identifier).isdigit():
            user = self.db.session.query(User).filter_by(id=identifier).one_or_none()
        elif '@' in str(identifier):
            user = self.db.session.query(User).filter_by(email=identifier).one_or_none()
        else:
            user = self.db.session.query(User).filter_by(username=identifier).one_or_none()
        if not user:
            abort(404, description=f'The user with this identifier not found')
            return
        return user
    
    def create_user(self, user: User):
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
            
    def delete_user(self, id):
        user = self.get_user(id)
        if not user:
            abort(404, description=f'The user with this identifier not found')
            return
        if user.is_deleted_user:
            abort(400, description='The user is already deleted')
        existing_access_token = self.db.session.query(UserToken).filter_by(user_id=id).one_or_none()
        if existing_access_token:
            jti = decode_token(existing_access_token.value).get('jti')
            blocked_jti = Blocklist(jti=jti)
            self.db.session.add(blocked_jti)
        user.is_deleted_user = True
        try:
            self.db.session.commit()
        except Exception as ex:
            self.db.session.rollback()
            abort(500, description=ex)

    def recover_user(self, id):
        user = self.get_user(id)
        if not user:
            abort(404, description=f'The user with this identifier not found')
            return
        if not user.is_deleted_user:
            abort(400, description='The user is already exist')
        existing_access_token = self.db.session \
            .query(UserToken) \
            .filter_by(user_id=id) \
            .order_by(desc(UserToken.id)) \
            .first() \
            .value
        if existing_access_token:
            existing_jti = decode_token(existing_access_token).get('jti')
            revoked_jti = self.db.session.query(Blocklist).filter_by(jti=existing_jti).one_or_none()
            self.db.session.delete(revoked_jti)
        user.is_deleted_user = False
        try:
            self.db.session.commit()
        except Exception as ex:
            self.db.session.rollback()
            abort(500, description=ex)

    def account_activation(self, id, isActive):
        user = self.repository.get_user(id)
        if not user:
            abort(404, description=f'The user with this identifier not found')
            return
        user.is_activated_account = isActive
        try:
            self.db.session.commit()
        except Exception as ex:
            self.db.session.rollback()
            abort(500, description=ex)
            
    def account_2FA(self, id, isEnabled):
        user = self.repository.get_user(id)
        if not user:
            abort(404, description=f'The user with this identifier not found')
            return
        user.is_2FA_enabled = isEnabled
        try:
            self.db.session.commit()
        except Exception as ex:
            self.db.session.rollback()
            abort(500, description=ex)
        