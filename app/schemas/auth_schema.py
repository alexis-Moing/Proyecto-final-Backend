from flask_restx import fields
from flask_restx.reqparse import RequestParser

class AuthRequestSchema:
    def __init__(self, namespace):
        self.ns = namespace
        
    
    # metodo para login de usuario
    def login(self):
        return self.ns.model('Auth SignIn', {
            'email' : fields.String(required=True, max_lenght=120),
            'password' : fields.String(required=True, max_lenght=18)
        })
        
    
    # Esquema para refresh token    
    def refresh(self):
        parser = RequestParser()
        parser.add_argument('Authorization', type=str , location='headers', help='Ex: Bearer {refresh_token}')
        return parser
    
    
    # Esquema para crear nueva contraseño
    def reset(self):
        return self.ns.model('Auth Reset Password', {
            'email' : fields.String(required=True)
        })