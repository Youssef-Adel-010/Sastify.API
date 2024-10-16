from flask_sqlalchemy import SQLAlchemy
from flask import abort, jsonify
from injector import inject
from app.dtos.register_dto import RegisterDto
from app.models.user import User
from app.repositories.user_management_repository import UserManagementRepository
from marshmallow import validate 
from werkzeug.security import generate_password_hash, check_password_hash


class UserManagementServices:
    @inject
    def __init__(
        self,
        register_dto: RegisterDto,
        user_management_repository: UserManagementRepository,
        users_table: User,
        db: SQLAlchemy):
        
        self.user_management_repository = user_management_repository
        self.register_dto = register_dto
        self.users_table = users_table
        self.db = db
        

    def register(self, data):
        errors = self.register_dto.validate(data)
        
        if errors:
            return jsonify({'errors': errors}) 
        
        user = self.register_dto.load(data)
        
        self.user_management_repository.register(user)

        return 0


    def verify_password(self, real_password, entered_password):
        return check_password_hash(real_password, entered_password)
    
    