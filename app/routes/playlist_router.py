from app import api
from flask_restx import Resource
from flask import request
from http import HTTPStatus
from app.schemas.playlist_schema import PlaylistRequestSchema
from app.controllers.playlist_controller import PlaylistController

playlist_ns = api.namespace(
    name='playlist',
    description='rutas para las playlist de los usuarios',
    path='/playlist'
)

schema_request = PlaylistRequestSchema(playlist_ns)


@playlist_ns.route('/<int:usuario_id>')
class Playlist(Resource):

    @playlist_ns.expect(schema_request.add_new_content(), validate=True)
    def post(self, usuario_id):
        '''Agregar contenido a mi lista'''
        controller = PlaylistController()
        return controller.save(usuario_id, request.json.get('title_content'), request.json)

    def get(self, usuario_id):
        '''Listar mi contenido guardado'''
        controller = PlaylistController()
        return controller.fetch_all(usuario_id)


@playlist_ns.route('/<int:id>')
class PlayById(Resource):
    def get(self, id):
        '''Escoger un contenido por su id'''

    def delete(self, id):
        '''Inhabbilitar un contenido de mi lista por su id'''
