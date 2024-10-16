from app import db
from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy import MetaData

metadata = MetaData(schema='security')

class UserToken(db.Model):
    __tablename__ = 'user_tokens'
    __table_args__ = (metadata,)

    # Columns
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    value = Column(String(), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Relations
    user = relationship('User', back_populates='tokens')
    
    # Representation
    def __repr__(self):
        return f"<UserTokens(user_id={self.user_id}, token='{self.name}', value='{self.value}')>"