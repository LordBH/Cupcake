from flask import render_template, abort, request, session, redirect, url_for
from flask_socketio import emit
from configurations.settings import ConfigClass
from chats import socket_io
from main.tools import users_context, slash
from os import path, makedirs
from werkzeug.utils import secure_filename
from . import from_main


extra = from_main


@extra.route('/')
def index_page():
    context = {}
    return render_template('base.html', context=context)


@extra.route(r'/config', methods=['POST'])
def user_conf():
    if request.method == 'POST':
        from models.models import User, db

        q = User.query.filter_by(id=session.get('user_id')).first()
        if q is None:
            abort(404)
        User.re_write_config(q)
        db.session.commit()

    return redirect(url_for('main.index_page'))


@extra.route(r'/upload_image', methods=['POST'])
def upload_img():
    u = str(session.get('user_id'))
    s = slash()
    f = request.files.get('image')
    if request.method == 'POST' and f:
        filename = secure_filename(f.filename)
        if filename.split('.')[-1] not in ['jpg', 'png', 'jpeg']:
            return render_template('reg/flash_message.html',
                                   context={'msg': 'Bad format, need: jpg, jpeg, png'})

        user_directory = ConfigClass.ABSOLUTE_IMAGES_FOLDER + s + u
        if not path.exists(user_directory):
            makedirs(user_directory)

        path_to_file = user_directory + s + u + '.jpg'
        f.save(path_to_file)
    return redirect(url_for('main.index_page'))


@socket_io.on('page', namespace='/main')
def page_context(data=None):
    from models.models import User

    current_id = session.get('user_id')
    query = User.query.filter_by(id=current_id).all()
    context = users_context(query)

    return emit('userData', context)


@socket_io.on('friends', namespace='/main')
def people_context(data=None):
    from models.models import User

    current_id = session.get('user_id')
    query = User.query.all()
    context = users_context(query, current_id)

    return emit('people', context)
