from app import db
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy import MetaData

metadata = MetaData(schema='security')

class UserRole(db.Model):
    __tablename__ = 'user_roles'
    __table_args__ = (metadata,)
    
    # Columns
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.id'), primary_key=True)
    
    # Representation
    def __repr__(self):
        return f"<UserId={self.user_id} - RoleId={self.role_id}>"