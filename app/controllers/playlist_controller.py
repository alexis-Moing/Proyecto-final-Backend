from app import db
from app.models.playlist_model import PlaylistModel
from app.schemas.playlist_schema import PlaylistResponseSchema
from http import HTTPStatus

class PlaylistController:
    def __init__(self):
        self.db = db
        self.model = PlaylistModel
        self.schema = PlaylistResponseSchema
        
    
    def save(self,usuario_id,title, body):
        try:
            record = self.model.where(usuario_id=usuario_id).first()
            content_exist = self.model.where(title_content=title).first()
                    
            if record:
                new_content = self.model.create(**body)
                self.db.session.add(new_content, content_exist)
                self.db.session.commit()
                    
                return {
                    'message' : f'El titulo {body["title_content"]} se a agreado a tu lista de reproduccion'
                }
                                
            # return {
            #     'message' : f'no se encontro el titulo {body["title_content"]}'
            # }
                
        except Exception as e:
            self.db.session.rollback()
            return {
                'message' : 'ocurrio un error',
                'error' : str(e)
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        finally:
            self.db.session.close()
            
            
    def fetch_all(self, id):
        try:
            record = self.model.where(id=id).first()
            
            if record:
                response = self.schema(many=False)
                return response.dump(record), HTTPStatus.OK
            
            return {
                'message' :f'no se encontro su lista de reproduccion'
            } , HTTPStatus.NOT_FOUND
        except Exception as e:
            return {
                'message' : 'ocurrio un error',
                'error' : str(e)
            }, HTTPStatus.INTERNAL_SERVER_ERROR
