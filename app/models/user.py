from app import db
from sqlalchemy import Column, String, Integer, Boolean, CheckConstraint
from sqlalchemy.orm import relationship, validates 
from sqlalchemy import MetaData

metadata = MetaData(schema='security')

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = (
        metadata,
        CheckConstraint(
            "first_name GLOB '[A-Za-z]*'",
            name='first_name_check'
        ),
        CheckConstraint(
            "last_name GLOB '[A-Za-z]*'",
            name='last_name_check'
        ),
        CheckConstraint(
            "username GLOB '^[a-zA-Z][a-zA-Z0-9_]*$'",
            name='username_check'
        )
    )

    
    # Columns
    id = Column(Integer, primary_key=True)
    title = Column(String(10), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(), nullable=False)
    is_2FA_enabled = Column(Boolean, nullable=False, default=False)
    

    # Relationships
    roles = relationship('Role', secondary='user_roles', back_populates='users')


    # Representation
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"