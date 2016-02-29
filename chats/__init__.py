from flask import Blueprint
from flask.ext.socketio import SocketIO


socket_io = SocketIO()

from_chats = Blueprint('chats', __name__, template_folder='templates',
                       static_folder='static', static_url_path='/%s' % __name__)

from . import routes
