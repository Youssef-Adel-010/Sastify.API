from flask import Blueprint
from flask_jwt_extended import jwt_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.get('/users')
@jwt_required()
def get_all_users():
    pass

@admin_bp.get('/users/<int:id>')
@jwt_required()
def get_user(id):
    pass

@admin_bp.post('/create')
@jwt_required()
def create(id):
    pass

@admin_bp.put('/update/<int:id>')
@jwt_required()
def create(id):
    pass

@admin_bp.delete('/delete/<int:id>')
@jwt_required()
def delete():
    pass

@admin_bp.post('/activate/<int:id>')
@jwt_required()
def activate():
    pass

@admin_bp.post('/deactivate/<int:id>')
@jwt_required()
def deactivate():
    pass

@admin_bp.post('/enable-2fa/<int:id>')
@jwt_required()
def enable_2fa():
    pass






















@admin_bp.get('/user-rules/<int:id>')
@jwt_required()
def user_rules(id):
    pass

@admin_bp.get('/user-tokens/<int:id>')
@jwt_required()
def user_tokens(id):
    pass

@admin_bp.get('/create-role')
@jwt_required()
def get_all_users():
    pass

@admin_bp.get('/blocklist')
@jwt_required()
def get_all_users():
    pass


@admin_bp.get('/all-users')
@jwt_required()
def get_all_users():
    pass

@admin_bp.get('/all-users')
@jwt_required()
def get_all_users():
    pass

