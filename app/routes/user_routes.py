from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from injector import inject
from app.responses.api_response import ApiResponse
from app.services.user_services import UserServices

user_bp = Blueprint('user', __name__)

@inject
@user_bp.post('/register')
def register(services: UserServices, response: ApiResponse):
    data = request.json
    required_fields = ['username', 'title', 'password', 'confirm_password', 'email', 'first_name', 'last_name']
    if any(field not in data for field in required_fields):
        return jsonify({'msg': 'Enter all required values (title, first_name, last_name, username, email, password, confirm_password)'})
    services.register(data)
    response.set_values(
        status_code=201,
        success=True,
        message='The user registered successfully, you must activate your account to continue.'
    )
    return response.to_json(), response.status_code

@inject
@user_bp.post('/login')
def login(services: UserServices, response: ApiResponse):
    data = request.json
    required_fields = ['username', 'password']
    if any(field not in data for field in required_fields):
        return jsonify({'msg': 'Enter all required values (username, password)'})
    token = services.login(data) 
    if token == '2FA':
        return jsonify({'msg': 'Enter the OTP in your mail box'})
    response.set_values(
        status_code=200,
        success=True,
        message='The account logged in successfully.',
        data={'access_token': token}
    )
    return response.to_json(), response.status_code

@inject
@user_bp.post('/logout')
@jwt_required()
def logout(services: UserServices, response: ApiResponse):
    services.logout()
    response.set_values(
        status_code=200,
        success=True,
        message='The account logged out successfully.'
    )
    return response.to_json(), response.status_code

@inject
@user_bp.post('/forgot-password')
def forgot_password(services: UserServices, response: ApiResponse):
    data = request.json
    if not 'email' in data:
        return jsonify({'msg': 'Enter all required values (email)'})
    email = data.get('email')
    services.forgot_password(email)
    response.set_values(
        status_code=200,
        success=True,
        message='Password reset email has been sent.'
    )
    return response.to_json(), response.status_code

@inject
@user_bp.post('/reset-password/<token>')
def reset_password(token, services: UserServices, response: ApiResponse):
    data = request.json
    required_fields = ['new_password', 'confirm_password']
    if any(field not in data for field in required_fields):
        return jsonify({'msg': 'Enter all required fields (new_password, confirm_password)'})
    services.reset_password(reset_token=token, data=data)
    response.set_values(
        status_code=200,
        success=True,
        message='The password changed successfully.'
    )
    return response.to_json(), response.status_code

@inject
@user_bp.put('/enable-2fa')
@jwt_required()
def enable_2fa(services: UserServices, response: ApiResponse):
    res = services.enable_2FA()
    if res == 'not_activated_account':
        return jsonify({'msg': 'Activate your account before taking this action'})
    response.set_values(
        status_code=200,
        success=True,
        message='Two factor authentication enabled successfully.'
    )
    return response.to_json(), response.status_code

@inject
@user_bp.put('/disable-2fa')
@jwt_required()
def disable_2fa(services: UserServices, response: ApiResponse):
    res = services.disable_2FA()    
    if res == 'not_activated_account':
        return jsonify({'msg': 'Activate your account before taking this action'})
    response.set_values(
        status_code=200,
        success=True,
        message='Two factor authentication disabled successfully.'
    )
    return response.to_json(), response.status_code

@inject
@user_bp.post('/otp-login')
def otp_login(services: UserServices, response: ApiResponse):
    data = request.json
    required_fields = ['username', 'otp']
    if any(field not in data for field in required_fields):
        return jsonify({'msg': 'Enter all required values (username, otp)'})
    username = data['username']
    otp = data['otp']
    token = services.handle_2FA_OTP_login(entered_otp=otp, username=username)
    response.set_values(
        status_code=200,
        success=True,
        message='The account logged in successfully.',
        data={'access_token': token}
    )
    return response.to_json(), response.status_code

@inject
@user_bp.get('/profile')
@jwt_required()
def get_current_user_profile(services: UserServices, response: ApiResponse):
    profile = services.get_current_user_profile()
    if profile == 'not_activated_account':
        return jsonify({'msg': 'Activate your account before taking this action'})
    response.set_values(
        status_code=200,
        success=True,
        message='User data retrieved successfully.',
        data=profile
    )
    return response.to_json(), response.status_code

@inject
@user_bp.put('/update')
@jwt_required()
def update(services: UserServices, response: ApiResponse):
    data = request.json
    updated_profile = services.update_user_data(data)
    if updated_profile == 'not_activated_account':
        return jsonify({'msg': 'Activate your account before taking this action'})
    response.set_values(
        status_code=200,
        success=True,
        message='User data updated successfully.',
        data=updated_profile
    )
    return response.to_json(), response.status_code

@inject
@user_bp.put('/change-password')
@jwt_required()
def change_password(services: UserServices, response: ApiResponse):
    data = request.json
    required_fields = ['new_password', 'confirm_password']
    if any(field not in data for field in required_fields):
        return jsonify({'msg': 'Enter all required values (new_password, confirm_password)'})
    res = services.change_password(data=data)
    if res == 'not_activated_account':
        return jsonify({'msg': 'Activate your account before taking this action'})
    response.set_values(
        status_code=200,
        success=True,
        message='The password changed successfully.'
    )
    return response.to_json(), response.status_code

@inject
@user_bp.get('/send-activation-code')
@jwt_required()
def send_activation_code(services: UserServices, response: ApiResponse):
    services.send_activation_code()
    return jsonify({'msg': 'Activation code has been set to your registered email'}), 200

@inject
@user_bp.put('/activate-account')
@jwt_required()
def activate_account(services: UserServices, response: ApiResponse):
    data = request.json
    if not 'otp' in data:
        return jsonify({'msg': 'Enter all required values (otp)'})
    print(data['otp'])
    services.activate_account(entered_otp=data.get('otp'))
    response.set_values(
        status_code=200,
        success=True,
        message='Account activated successfully.'
    )
    return response.to_json(), response.status_code