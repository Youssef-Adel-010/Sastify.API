from flask_jwt_extended import JWTManager
from flask_injector import inject
from app.repositories.user_management_repository import UserManagementRepository
from app.responses.api_response import ApiResponse
from app import db

def register_jwt_helper(jwt: JWTManager):
    
    @inject
    def user_management_repository(repository: UserManagementRepository):
        return repository
    
    
    @jwt.user_lookup_loader
    def user_lookup(_jwt_headers, jwt_data):
        identity = jwt_data['sub']

        user = UserManagementRepository(db).get_user_by_username(identity)
        return user
        
    
    @jwt.expired_token_loader
    def expired_token(jwt_header, jwt_data):
        response = ApiResponse()
        response.set_values(
            status_code = 401, 
            error = 'expired_token',
            message = 'The token has expired',
            success = False,
        )
        
        return response.to_json(), 401



    @jwt.invalid_token_loader
    def invalid_token(error):
        response = ApiResponse()
        response.set_values(
            status_code = 401,
            error = 'invalid_token',
            message = 'Signature verification failed',
            success = False,
        )
        
        return response.to_json(), 401
    


    @jwt.unauthorized_loader
    def unauthorized_loader(error):
        response = ApiResponse()
        response.set_values(
            status_code = 401,
            error = 'unauthorized_user',
            message = 'Request doesn\'t contain a valid token',
            success = False,
        )
        
        return response.to_json(), 401
    

