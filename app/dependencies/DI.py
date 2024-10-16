from flask import request
from flask_sqlalchemy import SQLAlchemy
from app.responses.api_response import ApiResponse
from app.models.user import User
from app.repositories.user_management_repository import UserManagementRepository 
from flask_injector import Binder, inject, singleton
from app.dtos.register_dto import RegisterDto
from app.services.user_management_services import UserManagementServices

@inject
def config(binder: Binder):
    
    from app import db
    binder.bind(SQLAlchemy, to=db, scope=singleton)
    binder.bind(User, to=User, scope=request)
    binder.bind(UserManagementRepository, to=UserManagementRepository, scope=request)
    binder.bind(UserManagementServices, to=UserManagementServices, scope=request)
    binder.bind(RegisterDto, to=RegisterDto)
    binder.bind(ApiResponse, to=ApiResponse)
    
    