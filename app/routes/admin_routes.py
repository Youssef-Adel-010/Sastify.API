from flask import Blueprint, jsonify, redirect, request, url_for
from flask_jwt_extended import jwt_required
from injector import inject
from app.responses.api_response import ApiResponse
from app.services.admin_services import AdminServices

admin_bp = Blueprint('admin', __name__)

@inject
@admin_bp.get('/get-all-users')
# @jwt_required()
def get_all_users(services: AdminServices, response: ApiResponse):
    users = services.get_all_users()
    response.set_values(
        data=users,
        status_code=200,
        success=True,
        message='All users data fetched successfully'
    )
    return response.to_json(), response.status_code    

@admin_bp.get('/get-user/<identifier>')
# @jwt_required()
def get_user(identifier, services: AdminServices, response: ApiResponse):
    user = services.get_user(identifier)
    response.set_values(
        data=user,
        status_code=200,
        success=True,
        message='All users data fetched successfully'
    )
    return response.to_json(), response.status_code

@admin_bp.post('/create-user')
# @jwt_required()
def create_user(services: AdminServices, response: ApiResponse):
    data = request.json
    required_fields = [
        'username',
        'title',
        'password',
        'confirm_password',
        'email', 
        'first_name',
        'last_name',
        'is_2FA_enabled',
        'is_activated_account']
    if any(field not in data for field in required_fields):
        return jsonify({'msg': 'Enter all required values (title, first_name, last_name, username, email, password, confirm_password, is_activated_account, is_2FA_enabled)'})
    services.create_user(data)
    response.set_values(
        status_code=201,
        success=True,
        message=f'The created successfully{', don\'t forget to activate account.' if data['is_activated_account']==False else '.'}'
    )
    return response.to_json(), response.status_code

@admin_bp.delete('/delete-user/<int:id>')
# @jwt_required()
def delete_user(id, services: AdminServices, response: ApiResponse):
    services.delete_user(id)
    response.set_values(
        status_code=200,
        success=True,
        message=f'The account deleted successfully.' 
    )
    return response.to_json(), response.status_code

@admin_bp.post('/recover-user/<int:id>')
# @jwt_required()
def recover_user(id, services: AdminServices, response: ApiResponse):
    services.recover_user(id)
    response.set_values(
        status_code=200,
        success=True,
        message=f'The account recovered successfully.' 
    )
    return response.to_json(), response.status_code
    
@admin_bp.post('/activate-account/<int:id>')
# @jwt_required()
def activate_account(id, services: AdminServices, response: ApiResponse):
    services.account_activation(id=id, isActive=True)
    response.set_values(
        status_code=200,
        success=True,
        message=f'The account activated successfully.' 
    )
    return response.to_json(), response.status_code
    
@admin_bp.post('/deactivate-account/<int:id>')
# @jwt_required()
def deactivate_account(id, services: AdminServices, response: ApiResponse):
    services.account_activation(id=id, isActive=False)
    response.set_values(
        status_code=200,
        success=True,
        message=f'The account deactivated successfully.' 
    )
    return response.to_json(), response.status_code

@admin_bp.post('/enable-2fa/<int:id>')
# @jwt_required()
def enable_2fa(id, services: AdminServices, response: ApiResponse):
    services.account_2FA(id=id, isEnabled=True)
    response.set_values(
        status_code=200,
        success=True,
        message=f'Two factor authentication enabled successfully.' 
    )
    return response.to_json(), response.status_code
    
@admin_bp.post('/disable-2fa/<int:id>')
# @jwt_required()
def disable_2fa(id, services: AdminServices, response: ApiResponse):
    services.account_2FA(id=id, isEnabled=False)
    response.set_values(
        status_code=200,
        success=True,
        message=f'Two factor authentication disabled successfully.' 
    )
    return response.to_json(), response.status_code
    
# @admin_bp.post('/change-user-password/<int:id>')
# @jwt_required()
# def change_user_password():
#     pass

# @admin_bp.get('/get-roles')
# def list_all_rules():
#     pass

# @admin_bp.get('/get-role/<int:id>')
# def list_user_rules():
#     pass

# @admin_bp.post('/create-role')
# def create_rule():
#     pass

# @admin_bp.put('/update-role/<int:id>')
# def create_rule():
#     pass

# @admin_bp.delete('/delete-role/<int:id>')
# def create_rule():
#     pass

# @admin_bp.post('/assign-role/<int:id>')
# def create_rule():
#     pass

# @admin_bp.post('/unassign-role/<int:id>')
# def create_rule():
#     pass

# @admin_bp.get('/get-user-roles/<int:id>')
# def get_user_roles():
#     pass

# @admin_bp.get('/get-user-tokens/<int:id>')
# def get_user_tokens():
#     pass

# @admin_bp.post('/revoke-token')
# def revoke_token():
#     pass

# @admin_bp.get('/blocklist')
# @jwt_required()
# def get_all_users():
#     pass