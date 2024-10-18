from app.responses.api_response import ApiResponse
from flask_injector import inject

def register_error_handlers(app):
    
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