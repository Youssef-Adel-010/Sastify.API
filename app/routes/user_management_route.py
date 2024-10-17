from flask import Blueprint, jsonify, request
from injector import inject

from app.responses.api_response import ApiResponse
from app.services.user_management_services import UserManagementServices

auth_bp = Blueprint('authentication', __name__)

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

    services.login(data)

    response.set_values(
        status_code=200,
        success=True,
        message='The account logged in successfully.'
    )
    
    return response.to_json(), response.status_code