from flask import Blueprint, jsonify, request
from injector import inject

from app.responses.api_response import ApiResponse
from app.services.user_management_services import UserManagementServices

auth_bp = Blueprint('authentication', __name__)

@inject
@auth_bp.post('/register')
def register(services: UserManagementServices, response: ApiResponse):
    data = request.json
    
    
    if services.register(data) != 0:
        return services.register(data)
    
     
    response.set_values(
        status_code=201,
        success=True,
        message='The user registered successfully'
    )
    
    return response.to_json(), response.status_code