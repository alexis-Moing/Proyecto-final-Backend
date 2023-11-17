from app.models import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, LargeBinary


class PlaylistModel(BaseModel):
    __tablename__ = 'Playlists'

    id = Column(Integer, primary_key=True, autoincrement=True)
    # user_name = Column(Integer, ForeignKey('users.name'))
    usuario_id = Column(Integer, ForeignKey('users.id'))
    # title = Column(String(255), unique=True, nullable=False)
    title_content = Column(String, ForeignKey('Content.title'))
    
 
