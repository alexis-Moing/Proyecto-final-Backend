from app import db, mail
from app.models.users_model import UserModel
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token
from secrets import token_hex
from os import getenv
from flask_mail import Message


class AuthController:
    def __init__(self):
        self.db = db
        self.model = UserModel

    def sign_in(self, body):
        try:
            email = body['email']
            # validamos la existencia del usuario
            record = self.model.where(email=email, status=True).first()
            # validacion de la contraseña ---------------
            if record:
                password = body['password']
                if record.check_password(password):
                    user_id = record.id
                    # agregacion del token access
                    access_token = create_access_token(identity=user_id)
                    refresh_token = create_refresh_token(identity=user_id)
                    return {
                        'message': 'as iniciado sesion aqui estan tus tokens:',
                        'access_token': access_token,
                        'refresh_token': refresh_token,
                        'status': "success"
                    }, HTTPStatus.OK
                return {
                    'message': 'la contraseña es incorrecta'
                }, HTTPStatus.UNAUTHORIZED
            # ------------------------------------------
            return {
                'message': f'no se reconoce el correo: {email}'
            }, HTTPStatus.NOT_FOUND

        except Exception as e:
            return {
                'message': 'ocurrio un error',
                "status": "failed",
                'error': str(e)
            }, HTTPStatus.INTERNAL_SERVER_ERROR

    def refresh_token(self, identity):
        try:
            access_token = create_access_token(identity=identity)
            return {
                'access_token': access_token
            }, HTTPStatus.OK

        except Exception as e:
            return {
                'message': 'ocurrio un error',
                'error': str(e)
            }, HTTPStatus.INTERNAL_SERVER_ERROR

    def password_reset(self, body):
        try:
            email = body['email']
            record = self.model.where(email=email, status=True).first()
            if record:
                new_password = token_hex(6)
                record.password = new_password
                record.hash_password()

                self.db.session.add(record)
                self.db.session.commit()

                # estructura del correo a enviar
                message = Message(
                    subject='Contraseña Actualizada',
                    sender=('CINEPLUS', getenv('MAIL_USERNAME')),
                    recipients=[email],
                    # body=f'Esta es tu nueva contraseña: {new_password}'
                    html=f'<h3>Esta es tu nueva contraseña: <b>{new_password}</b></h3>'
                )
                # enviando como tal el correo
                mail.send(message)

                return {
                    'message': 'La contraseña a sido cambiada, por favor revise su correo'
                }, HTTPStatus.OK

            return {
                'message': f'no se encontro el correo: {email}'
            }, HTTPStatus.NOT_FOUND
        except Exception as e:
            self.db.session.rollback()
            return {
                'message': 'ocurrio un error',
                'error': str(e)
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        finally:
            self.db.session.close()
