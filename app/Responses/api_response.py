from flask import jsonify

class ApiResponse:
    def set_values(self, success: bool=True, status_code: int=200, message: str='sastify', data: dict=None, error: str = 'no errors'):
        self.status_code = status_code
        self.message = message
        self.data = data
        self.success = success
        self.error = error
        
    def to_json(self):
        return jsonify({
            'status_code': self.status_code,
            'success': self.success,
            'message': self.message,
            'data': self.data,
            'error': self.error
        })