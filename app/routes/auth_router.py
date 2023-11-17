from app import api 
from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.auth_controller import AuthController
from app.schemas.auth_schema import AuthRequestSchema

auth_ns = api.namespace(
    name = 'Authentication',
    description = 'rutas para el tema de la autenticacion',
    path = '/auth'
)

schema_request = AuthRequestSchema(auth_ns)

@auth_ns.route('/signin')
class SignIn(Resource):
    @auth_ns.expect(schema_request.login(), validate=True)
    def post(self):
        '''Login de usuario'''
        controller = AuthController()
        return controller.sign_in(request.json)


   
@auth_ns.route('/token/refresh')
class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    @auth_ns.expect(schema_request.refresh(), validate=True)
    def post(self):
        '''Obtener nuevo access_token si este vencio'''
        #recuperamos el id para crear un nuevo access token
        identity = get_jwt_identity()
        controller = AuthController()
        return controller.refresh_token(identity)

    
@auth_ns.route('/password/reset')
class NewPassword(Resource):
    @auth_ns.expect(schema_request.reset(), validate=True)
    def post(self):
        '''Crear nueva contraseña del usuario'''
        controller = AuthController()
        return controller.password_reset(request.json)
