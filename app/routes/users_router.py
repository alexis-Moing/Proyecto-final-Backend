from app import api
from flask_restx import Resource
from flask import request
from http import HTTPStatus
from app.controllers.users_controller import UserController
from app.schemas.users_schema import UserRequestSchema
from flask_jwt_extended import jwt_required

user_ns = api.namespace(
    name='users',
    description='Rutas del modulo users',
    path='/users'
)

schema_request = UserRequestSchema(user_ns)

@user_ns.route('')
# para rutas protegidas con autenticacion
@user_ns.doc(security='Bearer')
class Users(Resource):
    @user_ns.expect(schema_request.create(), validate=True)
    def post(self):
        '''Creacion de usuarios'''
        controller = UserController()
        return controller.save(request.json)
    
    
    @jwt_required()
    @user_ns.expect(schema_request.all())
    def get(self):
        '''Listar todos los usuarios'''
        #imprime en terminal la paginacion
        query_params = schema_request.all().parse_args()
        controller = UserController()
        return controller.fetch_all(query_params)


@user_ns.doc(security='Bearer')
@user_ns.route('/<int:id>')
class UserById(Resource):
    @jwt_required()
    def get(self,id):
        '''Obtener un usuario por su id'''
        controller = UserController()
        return controller.find_by_id(id)
    
    
    @jwt_required()
    @user_ns.expect(schema_request.update(), validate=True)
    def patch(self, id):
        '''Actualizar un usuario por su id'''
        controller = UserController()
        return controller.update(id, request.json)
        
    
    @jwt_required()
    def delete(self, id):
        '''Inhabilitar un usuario por su id'''
        controller = UserController()
        return controller.remove(id)    