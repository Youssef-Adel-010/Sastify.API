from app import db
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy import MetaData

metadata = MetaData(schema='security')

class Role(db.Model):
    __tablename__ = 'roles'
    __table_args__ = (metadata,)
        
    # Columns
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    
    
    # Relations
    users = relationship('User', secondary='user_roles', back_populates='roles')
    
    
    # Representation
    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}')>"