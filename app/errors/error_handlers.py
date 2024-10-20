from app.responses.api_response import ApiResponse
def register_error_handlers(app):
    def create_error_response(status_code, error, message):
        response = ApiResponse()
        response.set_values(
            success=False,
            error=error,
            status_code=status_code,
            message=message
        )
        return response.to_json(), status_code

    # Error handling mappings
    error_handlers = {
        404: ('Not Found', 'The requested resource was not found.'),
        401: ('Unauthorized Access', ''),
        400: ('Bad Request', ''),
        409: ('Conflict', 'A conflict occurred with existing data.'),
        500: ('Internal Server Error', 'An unexpected error occurred.')
    }

    for status_code, (error_title, default_message) in error_handlers.items():
        @app.errorhandler(status_code)
        def handle_error(e, status_code=status_code, error_title=error_title, default_message=default_message):
            message = e.description if hasattr(e, 'description') else default_message      
            return create_error_response(status_code, error_title, message)