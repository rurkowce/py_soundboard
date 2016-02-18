from threading import Thread
from six.moves.queue import Queue
from flask import Flask, url_for, current_app, g
from flask_restful import Api, Resource

api = Api()


@api.resource('/')
class Index(Resource):
    def get(self):
        board = current_app.board
        return {'sound_sets': list(board.shared_online)}


@api.resource('/sound_set/<string:set_name>', endpoint='sound_set')
class SoundSet(Resource):
    def get(self, set_name):
        board = current_app.board
        sound_set = board.shared_online.get(set_name)
        if not sound_set:
            return '>:'

        return {'sounds': [s.name for s in sound_set.sounds.values()]}


# @api.resource('/stats')
# class Stats(Resource)


@api.resource('/play/<string:set_name>/<string:sound_name>', endpoint='play')
class Play(Resource):
    def get(self, set_name, sound_name):
        board = current_app.board
        sound_set = board.shared_online.get(set_name)
        sound = sound_set.sounds[sound_name]
        sound.play()


class FlaskApp:
    def __init__(self, board, settings):
        """:type board: soundboard.board.Board"""
        self.board = board
        self.settings = settings
        self.queue = Queue()

        self.app = Flask(__name__)
        self.app.board = board
        self.api = api.init_app(self.app)

    def run(self, *args, **kwargs):
        self.app.run(*args, **kwargs)


class HTTPThread(Thread):

    def __init__(self, board, settings):
        super(HTTPThread, self).__init__()
        self.daemon = True
        self.settings = settings
        self.app = FlaskApp(board, settings)
        self.queue = self.app.queue

    def run(self):
        self.app.run(self.settings.http_ip, self.settings.http_port, False)
