from flask_jwt_extended import JWTManager
from flask_injector import inject
from app.models.blocklist import Blocklist
from app.repositories.user_repository import UserRepository
from app.responses.api_response import ApiResponse
from app import db

def register_jwt_helper(jwt: JWTManager):
    @jwt.user_lookup_loader
    def user_lookup(_jwt_headers, jwt_data):
        identity = jwt_data['sub']
        user = UserRepository(db).get_user_by_username(identity)
        return user
   
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        return db.session.query(Blocklist).filter_by(jti=jti).one_or_none()
   
    @jwt.expired_token_loader
    def expired_token(jwt_header, jwt_data):
        response = ApiResponse()
        response.set_values(
            status_code = 401, 
            error = 'unauthorized_user',
            message = 'Expired token',
            success = False
        )
        return response.to_json(), 401

    @jwt.invalid_token_loader
    def invalid_token(error):
        response = ApiResponse()
        response.set_values(
            status_code = 401,
            error = 'unauthorized_user',
            message = 'Invalid token',
            success = False
        )
        return response.to_json(), 401

    @jwt.unauthorized_loader
    def unauthorized_loader(error):
        response = ApiResponse()
        response.set_values(
            status_code = 401,
            error = 'unauthorized_user',
            message = 'Invalid token',
            success = False
        )
        return response.to_json(), 401