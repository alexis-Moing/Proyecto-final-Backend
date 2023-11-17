from os import getenv
from datetime import timedelta

class BaseConfig:
    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIIFCATIONS = False
    
    # clave para los tokens de jwt
    JWT_SECRET_KEY = getenv('SECRET_KEY')
    
    # variables para el tema de contraseña enviada a correo
    # conectar al servidor de gmail 
    MAIL_SERVER =getenv('MAIL_SERVER')
    MAIL_PORT = getenv('MAIL_PORT')
    MAIL_USE_TLS =getenv('MAIL_USE_TLS')
    MAIL_USERNAME =getenv('MAIL_USERNAME')
    MAIL_PASSWORD = getenv('MAIL_PASSWORD')

class DevelopmentConfig(BaseConfig):
    # duracion del access token en development
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(hours=1)
    MAIL_DEBUG=True

environment = {
    'development' : DevelopmentConfig
}