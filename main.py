from app import app, db
from app import routes
from app.models import BaseModel

BaseModel.set_session(db.session)