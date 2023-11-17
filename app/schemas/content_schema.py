from flask_restx import fields
from flask_restx.reqparse import RequestParser
from app.models.content_model import ContentModel
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask_restx import Namespace

class ContentRequestSchema:
    def __init__(self, namespace):
        self.ns = namespace
        
     
    def all(self):
        parser = RequestParser()
        parser.add_argument('page', type=int, location='args')
        parser.add_argument('per_page', type=int, location='args')    
        return parser 
    
        
    def create(self):
        return self.ns.model('Content Create', {
            'title' : fields.String(required=True, max_lenght=120),
            'description' : fields.String(required=True, max_lenght=250),
            'genre' : fields.String(required=True, max_lenght=120),
            'picture': fields.String(required=True, description="app/images")
        })
        
    def update(self):
        return self.ns.model('Content update', {
            'title' : fields.String(required=False, max_lenght=120),
            'description' : fields.String(required=False, max_lenght=250),
            'genre' : fields.String(required=False, max_lenght=120)
        })
        

class ContentResponseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ContentModel

