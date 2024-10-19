from app import db
from sqlalchemy import Column, String, Integer, Boolean, CheckConstraint, DateTime, func
from sqlalchemy.orm import relationship, validates 
from sqlalchemy import MetaData
import pyotp

metadata = MetaData(schema='security')

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = (
        metadata,
        CheckConstraint(
            "title REGEXP '^[a-zA-Z]+$'",
            name='title_check'
        ),
        CheckConstraint(
            "first_name REGEXP '^[a-zA-Z]+$'",
            name='first_name_check'
        ),
        CheckConstraint(
            "last_name REGEXP '^[a-zA-Z]+$'",
            name='last_name_check'
        ),
        CheckConstraint(
            "email REGEXP '^[a-zA-Z0-9._-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'",
            name='email_check'
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
    registered_on = Column(DateTime, nullable=False, default=func.now())
    is_2FA_enabled = Column(Boolean, nullable=False, default=False)
    is_activated_account = Column(Boolean, nullable=False, default=False)
    is_deleted_user = Column(Boolean, nullable=False, default=False)
    secret_key = Column(String(), nullable=False, default=pyotp.random_base32())
    
    # Relationships
    roles = relationship('Role', secondary='user_roles', back_populates='users', cascade='all, delete')
    tokens = relationship('UserToken', back_populates='user', cascade='all, delete-orphan')

    # Representation
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"