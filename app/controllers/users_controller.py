from app import db
from app.models.users_model import UserModel
from http import HTTPStatus
from app.schemas.users_schema import UserResponseSchema

class UserController:
    def __init__(self):
        self.db = db
        self.model = UserModel
        self.schema = UserResponseSchema
    
    def save(self, body):
        try:
            record_new = self.model.create(**body)
            record_new.hash_password()
            self.db.session.add(record_new)
            self.db.session.commit()
            
            return {
                'message' : f'el usuario {body["name"]} se creo con exito'
            }, HTTPStatus.CREATED
            
        except Exception as e:
            self.db.session.rollback()
            return {
                'message' : 'a ocurrido un error',
                'error': str(e)
            }, HTTPStatus.INTERNAL_SERVER_ERROR
            
        finally:
            self.db.session.close()
            
    
    def fetch_all(self, query_params):
        # paginacion
        try:
            page = query_params['page']
            per_page = query_params['per_page']
            
            records = self.model.where(status=True).order_by('id').paginate(
                page = page,
                per_page = per_page
            )
            
            response = self.schema(many=True)
            
            return {
                'results': response.dump(records.items),
                
                # datos de paginacion
                'pagination' : {
                    'totalRecords' : records.total,
                    'totalPages' : records.pages,
                    'porPage' : records.per_page,
                    'currentPage' : records.page
                }
            }, HTTPStatus.OK 
        except Exception as e:
            return {
                'message' : 'ocurrio un error',
                'error' : str(e)
            }, HTTPStatus.INTERNAL_SERVER_ERROR
            
    
    def find_by_id(self, id):
        try:
            record = self.model.where(id=id, status=True).first()
            
            if record:
                response = self.schema(many=False)
                return response.dump(record), HTTPStatus.OK
            
            return {
                'message' : f'no se encontro un usuario con el ID: {id}'
            }, HTTPStatus.NOT_FOUND
            
        except Exception as e:
            return {
                'message' : 'a ocurrido un error',
                'error' : str(e)
            }, HTTPStatus.NOT_FOUND
            
            
    def update(self, id, body):
        try: 
            record = self.model.where(id=id, status=True).first()
            
            if record:
                record.update(**body)
                self.db.session.add(record)
                self.db.session.commit()
                
                return {
                    'message':f'el usuario con el ID: {id} a sido actualizado' 
                }, HTTPStatus.OK
                
            return {
                'message':f'no se encontro el usuario con el ID: {id}'
            }, HTTPStatus.NOT_FOUND
            
        except Exception as e:
            self.db.session.rollback()
            return {
                'message': 'ocurrio un error',
                'error' : str(e)
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        finally:
            self.db.session.close()
            
    def remove(self,id):
        try:
            record = self.model.where(id=id, status=True).first()
            
            if record:
                record.update(status=False)
                self.db.session.add(record)
                self.db.session.commit()
                return {
                    'message': f'El usuario con el ID: {id} a sido inhabilitado'
                }, HTTPStatus.OK 
                
            return {
                'message':f'no se encontro el usuario con el ID: {id}'
            }, HTTPStatus.NOT_FOUND
            
        except Exception as e:
            self.db.session.rollback()
            return {
                'message': 'ocurrio un error',
                'error': str(e)
            }, HTTPStatus.INTERNAL_SERVER_ERROR 
        finally:
            self.db.session.close()
            
    
    def profile_me(self,identity):
        try:
            record = self.model.where(id=identity).first()
            response = self.schema(many=False)
            return response.dump(record), HTTPStatus.OK
        except Exception as e:
            return {
                'message' : 'a ocurrido un error',
                'error' : str(e)
            }, HTTPStatus.INTERNAL_SERVER_ERROR