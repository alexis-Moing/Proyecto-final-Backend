from app import api
from flask_restx import Resource
from flask import request
from http import HTTPStatus
from app.schemas.content_schema import ContentRequestSchema
from app.controllers.content_controller import ContentController
from flask_jwt_extended import jwt_required

content_ns=api.namespace(
    name = 'Content',
    description = 'Rutas del contenido de mi aplicacion',
    path = '/content'
)

schema_request = ContentRequestSchema(content_ns)

@content_ns.route('')
@content_ns.doc(security='Bearer')
class Contenido(Resource):
    @content_ns.expect(schema_request.create(), validate=True)
    def post(self):
        '''Crear un nuevo contenido'''
        controller = ContentController()
        return controller.save(request.json)
        
    
    @jwt_required()
    @content_ns.expect(schema_request.all())
    def get(self):
        '''Listar todo el contenido'''
        query_params = schema_request.all().parse_args()
        controller = ContentController()
        return controller.fetch_all(query_params)
        

@content_ns.doc(security='Bearer')   
@content_ns.route('<title>')
class ContentById(Resource):
    @jwt_required()
    def get(self, title):
        '''Encontrar un contenido por su titulo'''
        controller = ContentController()
        return controller.content_by_title(title)
        
    
    @jwt_required()
    @content_ns.expect(schema_request.update(), validate=True)    
    def patch(self, title):
        '''Actualizar un contenido por su titulo'''
        controller = ContentController()
        return controller.update(title, request.json)
        
    
    @jwt_required()    
    def delete(self, title):
        '''Inhabilitar un contenido por su titulo'''
        controller = ContentController()
        return controller.remove(title)