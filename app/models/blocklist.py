from app import db
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy import MetaData

metadata = MetaData(schema='security')

class Blocklist(db.Model):
    __tablename__ = 'blocklist'
    __table_args__ = (metadata,)
    
    # Columns
    id = Column(Integer, primary_key=True)
    jti = Column(String(), nullable=False, unique=True)
    
    # Representation
    def __repr__(self):
        return f"<blocked_token={self.role_id}>"