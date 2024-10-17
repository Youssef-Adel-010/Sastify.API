from flask_sqlalchemy import SQLAlchemy
from flask import abort, jsonify
from injector import inject
from app.dtos.login_dto import LoginDto
from app.dtos.register_dto import RegisterDto
from app.models.user import User
from app.repositories.user_management_repository import UserManagementRepository


class UserManagementServices:
    @inject
    def __init__(
        self,
        register_dto: RegisterDto,
        login_dto: LoginDto,
        repository: UserManagementRepository,
        users_table: User,
        db: SQLAlchemy):
        
        self.repository = repository
        self.register_dto = register_dto
        self.login_dto = login_dto
        self.users_table = users_table
        self.db = db
        

    def register(self, data):
        errors = self.register_dto.validate(data)
        
        if errors:
            abort(400, description={'ValidationErrors': errors})
            return
        
        user = self.register_dto.load(data)
        
        self.repository.register(user)
        
    def login(self, data):
        errors = self.login_dto.validate(data)
        
        if errors:
            abort(401, description='Invalid credentials')
            return
        
        user = self.login_dto.load(data)
        self.repository.login(user)
        

    # def verify_password(self, real_password, entered_password):
    #     return check_password_hash(real_password, entered_password)
    
    