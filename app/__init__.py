from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from app.config import environment
from flask_migrate import Migrate
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS

FLASK_ENV = getenv('FLASK_ENV')
# llama a la clase DevelopmentConfig segun la clave environment
ENVIRONMENT = environment[FLASK_ENV]

# aqui hemos instanciado flask
app = Flask(__name__)
CORS(app, allow_headers=["Content-Type"])

app.config.setdefault("CORS_ALLOW_ORIGINS", "*")
app.config.setdefault("CORS_ALLOW_HEADERS", ["Content-Type", "Authorization"])
app.config.setdefault("CORS_ALLOW_METHODS", ["GET", "POST", "PUT", "DELETE"])


app.config.from_object(ENVIRONMENT)

# Autenticaciones para rutas protegidas
authorizations = {
    # authorization: bearer (access token)
    'Bearer' : {
        'type' : 'apiKey',
        'in' : 'header',
        'name' : 'Authorization'
    }
}

# Usando flask-restx para
api = Api(
    app,
    title= 'Api Cineplus',
    version= '0.1',
    description='Endpoints del backend de Cineplus',
    doc='/swagger-ui',
    authorizations=authorizations
)


db = SQLAlchemy(app)

migrate = Migrate(app, db)

jwt = JWTManager(app)

mail = Mail(app)