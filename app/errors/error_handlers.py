from app.responses.api_response import ApiResponse
from flask_injector import inject

def register_error_handlers(app):
    
    # JWT error handlers
    # using manual object creation (special case)

    # @jwt.expired_token_loader
    # def expired_token_handler(jwt_header, jwt_data):
    #     response = ApiResponse()
    #     response.set_values(
    #         status_code = 401, 
    #         error = 'expired_token',
    #         message = 'The token has expired',
    #         success = False,
    #     )
        
    #     return response.to_json(), 401

    # @jwt.invalid_token_loader
    # def invalid_token_handler(error):
    #     response = ApiResponse()
    #     response.set_values(
    #         status_code = 401,
    #         error = 'invalid_token',
    #         message = 'Signature verification failed',
    #         success = False,
    #     )
        
    #     return response.to_json(), 401
    

    # @jwt.unauthorized_loader
    # def unauthorized_loader_handler(error, response: ApiResponse):
    #     # response = ApiResponse()
    #     response.set_values(
    #         status_code = 401,
    #         error = 'unauthorized_user',
    #         message = 'Request doesn\'t contain a valid token',
    #         success = False,
    #     )
        
    #     return response.to_json(), 401
    


    # Status codes error handlers
    
    @inject
    @app.errorhandler(404)
    def handle_404_not_found(e, response: ApiResponse):
        response.set_values(
            success = False,
            error = 'Not Found',
            status_code = 404,
            message = e.description if hasattr(e, 'description') else 'The requested resource was not found.'
            
        )
        
        return response.to_json(), 404


    @inject
    @app.errorhandler(401)
    def handle_401_unauthorized_access(e, response: ApiResponse):
        response.set_values(
            success = False,
            error = 'Unauthorized Access',
            status_code = 401,
            message = e.description if hasattr(e, 'description') else ''
            
        )
        
        return response.to_json(), 401


    @inject
    @app.errorhandler(400)
    def handle_400_bad_request(e, response: ApiResponse):
        response.set_values(
            success = False, 
            error = 'Bad Request',
            status_code = 400,
            message = e.description if hasattr(e, 'description') else ''
        )    
        
        return response.to_json(), 400


    @inject
    @app.errorhandler(409)
    def handle_409_conflict(e, response: ApiResponse):
        response.set_values(
            success = False, 
            error = 'Conflict',
            status_code = 409,
            message = e.description if hasattr(e, 'description') else 'a conflict happened with existing data.'
        )   

        return response.to_json(), 409


    @inject
    @app.errorhandler(500)
    def handle_500_internal_server_error(e, response: ApiResponse):
        
        response.set_values(
            success = False, 
            error = 'Internal Server Error',
            status_code = 500,
            message = e.description if hasattr(e, 'description') else 'An unexpected error occurred.'
        )

        return response.to_json(), 500