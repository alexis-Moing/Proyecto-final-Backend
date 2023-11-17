from app import db
from app.models.content_model import ContentModel
from http import HTTPStatus
from app.schemas.content_schema import ContentResponseSchema

class ContentController:
    def __init__(self):
        self.db = db
        self.model = ContentModel
        self.schema = ContentResponseSchema
        
    
    def save(self, body):
        try:
            record_new = self.model.create(**body)
            self.db.session.add(record_new)
            self.db.session.commit()
            
            return {
                'message' : 'el contenido se agrego con exito'
            }, HTTPStatus.OK 
        
        except Exception as e:
            self.db.session.rollback()
            return {
                'message': 'ocurrio un error',
                'error' : str(e)
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        finally:
            self.db.session.close()
            
    
    def fetch_all(self, query_params):
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
            
            
    def content_by_title(self, title):
        try:
            
            title_lower = title.lower()
            
            record = self.model.query.filter(db.func.lower(self.model.title).ilike(title_lower), self.model.status == True).first()
            
            if record:
                response = self.schema(many=False)
                return response.dump(record), HTTPStatus.OK
            
            return {
                'message' : f'no se encontro el titulo: {title}'
            }, HTTPStatus.NOT_FOUND
            
        except Exception as e:
            return {
                'message' : 'a ocurrido un error',
                'error' : str(e)
            }, HTTPStatus.NOT_FOUND
            
            
    def update(self, title, body):
        try: 
            title_lower = title.lower()
            
            record = self.model.query.filter(db.func.lower(self.model.title).ilike(title_lower), self.model.status == True).first()
            
            if record:
                record.update(**body)
                self.db.session.add(record)
                self.db.session.commit()
                
                return {
                    'message':f'el contenido: {title} a sido actualizado' 
                }, HTTPStatus.OK
                
            return {
                'message':f'no se encontro el titulo: {title}'
            }, HTTPStatus.NOT_FOUND
            
        except Exception as e:
            self.db.session.rollback()
            return {
                'message': 'ocurrio un error',
                'error' : str(e)
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        finally:
            self.db.session.close()
            
            
    def remove(self,title):
        try:
            title_lower = title.lower()
            
            record = self.model.query.filter(db.func.lower(self.model.title).ilike(title_lower), self.model.status == True).first()
            
            if record:
                record.update(status=False)
                self.db.session.add(record)
                self.db.session.commit()
                return {
                    'message': f'El titulo: {title} a sido inhabilitado'
                }, HTTPStatus.OK 
                
            return {
                'message':f'no se encontro el titulo: {title}'
            }, HTTPStatus.NOT_FOUND
            
        except Exception as e:
            self.db.session.rollback()
            return {
                'message': 'ocurrio un error',
                'error': str(e)
            }, HTTPStatus.INTERNAL_SERVER_ERROR 
        finally:
            self.db.session.close()