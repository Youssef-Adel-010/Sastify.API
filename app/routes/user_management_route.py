from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from injector import inject
from app.responses.api_response import ApiResponse
from app.services.user_management_services import UserManagementServices

auth_bp = Blueprint('auth', __name__)

@inject
@auth_bp.post('/register')
def register(services: UserManagementServices, response: ApiResponse):
    data = request.json
    
    services.register(data)
        
    response.set_values(
        status_code=201,
        success=True,
        message='The user registered successfully.'
    )
    
    return response.to_json(), response.status_code


@inject
@auth_bp.post('/login')
def login(services: UserManagementServices, response: ApiResponse):
    data = request.json

    if services.login(data) == '2FA':
        return jsonify({'message': 'Enter the OTP in your mail box'})

    response.set_values(
        status_code=200,
        success=True,
        message='The account logged in successfully.'
    )
    
    return response.to_json(), response.status_code


@inject
@auth_bp.post('/forgot_password')
def forgot_password(services: UserManagementServices, response: ApiResponse):
    data = request.json
    email = data.get('email')
    
    services.forgot_password(email)
    response.set_values(
        status_code=200,
        success=True,
        message='Password reset email has been sent.'
    )
    
    return response.to_json(), response.status_code



@inject
@auth_bp.post('/reset_password/<token>')
def reset_password(token, services: UserManagementServices, response: ApiResponse):
    new_password = request.json['password']
    services.reset_password(reset_token=token, new_password=new_password)
    response.set_values(
        status_code=200,
        success=True,
        message='The password changed successfully.'
    )
    return response.to_json(), response.status_code



@inject
@auth_bp.post('/enable_2fa')
@jwt_required()
def enable_2fa(services: UserManagementServices, response: ApiResponse):
    services.enable_2FA()
    response.set_values(
        status_code=200,
        success=True,
        message='Two factor authentication enabled successfully.'
    )
    return response.to_json(), response.status_code


@inject
@auth_bp.post('/otp_login')
def otp_login(services: UserManagementServices, response: ApiResponse):
    data = request.json
    username = data['username']
    otp = data['otp']
    
    services.handle_2FA_OTP_login(entered_otp=otp, username=username)
    
    response.set_values(
        status_code=200,
        success=True,
        message='The account logged in successfully.'
    )
    
    return response.to_json(), response.status_code
