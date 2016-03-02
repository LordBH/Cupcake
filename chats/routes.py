from flask import session
from flask.ext.socketio import emit, join_room, leave_room
from .tools import compare
from . import from_chats, socket_io


main = from_chats


@socket_io.on('joined', namespace='/chat')
def joined(data):
    user_2 = data.get('id')
    if user_2 is None:
        return emit('status', {'flag': False, 'msg': 'id is empty'})
    try:
        user_2 = int(user_2)
    except ValueError:
        return emit('status', {'flag': False, 'msg': 'id is not int'})
    user_1 = session.get('user_id')

    extra = compare(user_1, user_2)

    room_id = '%d|%d' % extra
    if session.get('rooms') is None:
        session['rooms'] = []

    session['rooms'].append(room_id)

    join_room(room_id)

    emit('status', {'flag': True, 'msg': session.get('user_first_name') + ' has entered the room.'}, room=room_id)


@socket_io.on('message', namespace='/chat')
def message(data):
    from models.chat import Rooms, db

    room_id = data.get('room')
    if room_id is None:
        return emit('status', {'flag': False, 'msg': 'room is empty'})

    a = room_id.split('|')
    user_1 = session.get('user_id')

    if a[0] == str(user_1):
        q = Rooms(room_id, user1_mes=data.get('msg'))
    else:
        q = Rooms(room_id, user2_mes=data.get('msg'))
    db.session.add(q)
    db.session.commit()

    emit('message', {'flag': True, 'msg': data.get('msg')}, room=room_id)


@socket_io.on('left', namespace='/chat')
def left(data):

    room_id = data.get('room_id')
    if room_id is None:
        return emit('status', {'flag': False, 'msg': 'room_id is empty'})

    leave_room(room_id)

    emit('status', {'msg': data.get('first_name') + ' has left the room.'}, room=room_id)
