from app.models import BaseModel
from sqlalchemy import Column, Integer, String, Text, Boolean, LargeBinary, VARCHAR

class ContentModel(BaseModel):
    __tablename__ = 'Content'
    
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255),unique=True, nullable=False)
    description = Column(Text)
    genre = Column(String(100))
    picture = Column(VARCHAR(255))
    status = Column(Boolean, default=True)
    