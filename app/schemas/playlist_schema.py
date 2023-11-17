from flask_restx import fields
from flask_restx.reqparse import RequestParser
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.playlist_model import PlaylistModel

class PlaylistRequestSchema:
    def __init__(self, namespace):
        self.ns = namespace
        
        
    def add_new_content(self):
        return self.ns.model('Añadir Contenido', {
            'title_content' : fields.String(required=True, max_lenght=120)    
        })
        
class PlaylistResponseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PlaylistModel