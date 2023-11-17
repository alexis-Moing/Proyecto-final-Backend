from flask_restx import fields
from flask_restx.reqparse import RequestParser
from app.models.users_model import UserModel
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class UserRequestSchema:
    def __init__(self, namespace):
        self.ns = namespace
    
    
    # metodo para la paginacion en las rutas
    def all(self):
        parser = RequestParser()
        parser.add_argument('page', type=int, default=1, location='args')
        parser.add_argument('per_page', type=int, default=5, location='args')    
        return parser
    
    
    def create(self):
        return self.ns.model('User Create', {
            'name': fields.String(required=True, max_lenght=120),
            'lastname': fields.String(required=True, max_lenght=150),
            'email': fields.String(required=True, max_lenght=160),
            'password': fields.String(required=True, max_lenght=18)
        })
        
    def update(self):
        return self.ns.model('User Update', {
            'name': fields.String(required=True, max_lenght=120),
            'lastname': fields.String(required=True, max_lenght=150),
            'email': fields.String(required=True, max_lenght=160),
            'password': fields.String(required=True, max_lenght=18)
        })
        
        
class UserResponseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        exclude = ['password']