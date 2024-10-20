from flask import request
from flask_sqlalchemy import SQLAlchemy
from app.dtos.login_dto import LoginDto
from app.responses.api_response import ApiResponse
from app.models.user import User
from app.repositories.user_repository import UserRepository 
from flask_injector import Binder, inject, singleton
from app.dtos.register_dto import RegisterDto
from app.services.user_services import UserServices

@inject
def config(binder: Binder):
    
    from app import db
    binder.bind(SQLAlchemy, to=db, scope=singleton)
    binder.bind(User, to=User, scope=request)
    binder.bind(UserRepository, to=UserRepository, scope=request)
    binder.bind(UserServices, to=UserServices, scope=request)
    binder.bind(RegisterDto, to=RegisterDto)
    binder.bind(ApiResponse, to=ApiResponse)
    binder.bind(LoginDto, to=LoginDto)
    