from app.models import BaseModel
from sqlalchemy import Column, Integer, String, Boolean
from bcrypt import hashpw, gensalt, checkpw

class UserModel(BaseModel):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120))
    lastname = Column(String(120))
    email = Column(String(160), unique=True)
    password = Column(String(255))
    status = Column(Boolean, default=True)
    
    # metodo para encriptacion de contraseñas
    def hash_password(self):
        password_encode = self.password.encode('utf-8')
        password_hash = hashpw(password_encode, gensalt(rounds=10))
        self.password = password_hash
        self.password = password_hash.decode('utf-8')
    

    # validar contraseña
    def check_password(self, password):
        return checkpw(
            password.encode('utf-8'),
            self.password.encode('utf-8')
        )
    
