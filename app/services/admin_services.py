from flask import abort
from flask_jwt_extended import decode_token
from flask_sqlalchemy import SQLAlchemy
from injector import inject
from app.dtos.create_user_admin_dto import CreateUserAdminDto
from app.models.blocklist import Blocklist
from app.models.user import User
from app.models.user_token import UserToken
from app.repositories.admin_repository import AdminRepository
from app.schemas.all_users_admin_schema import AllUsersAdminSchema
from app.schemas.user_admin_schema import UserAdminSchema


class AdminServices:
    @inject
    def __init__(
        self,
        db: SQLAlchemy,
        repository: AdminRepository,
        all_users_schema: AllUsersAdminSchema,
        create_user_admin_dto: CreateUserAdminDto,
        user_admin_schema: UserAdminSchema):
        self.create_user_admin_dto = create_user_admin_dto
        self.user_admin_schema = user_admin_schema
        self.db = db
        self.repository = repository
        self.all_users_schema = all_users_schema
        
    def get_all_users(self):
        users = self.repository.get_all_users()
        users = self.all_users_schema.dump(users, many=True)
        return users
    
    def get_user(self, identifier):
        user = self.repository.get_user(identifier)
        user = self.user_admin_schema.dump(user)
        return user

    def create_user(self, data):
        errors = self.create_user_admin_dto.validate(data) 
        if errors:
            abort(400, description={'ValidationErrors': errors})
            return
        user = self.create_user_admin_dto.load(data)
        self.repository.create_user(user)
        
    def delete_user(self, id):
        self.repository.delete_user(id)
            
    def account_activation(self, id, isActive):
        self.repository.account_activation(id, isActive)
    
    def account_2FA(self, id, isEnabled):
        self.repository.account_2FA(id=id, isEnabled=isEnabled)
        
    def recover_user(self, id):
        self.repository.recover_user(id)