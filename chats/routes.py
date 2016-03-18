from flask.ext.socketio import emit, join_room
from flask import session
from .tools import compare, connecting, take_message, save_room, save_message, control_user_online
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
        return emit('status', {'flag': False, 'msg': 'ValueError : id is not int'})
    except TypeError:
        return emit('status', {'flag': False, 'msg': 'TypeError'})

    user_1 = session.get('user_id')

    extra = compare(user_1, user_2)

    room_id = '%d|%d' % extra

    session.setdefault('rooms', [])

    if room_id not in session['rooms']:
        join_room(room_id)
        session['rooms'].append(room_id)
        emit('unique_wire', {'flag': True, 'id': user_2, 'user': user_1}, room=user_2)
        save_room(user_1, user_2, room=room_id)

    chat = take_message(room_id, extra, number=0)

    context = {
        'flag': True,
        'room': room_id,
        'history': chat,
        'id': user_2,
    }

    emit('status', context)


@socket_io.on('message', namespace='/chat')
def message(data):
    room_id = data.get('room')
    if room_id is None:
        return emit('send_Message', {'flag': False, 'msg': 'room is empty'})

    msg = data.get('msg')

    context = {
        'flag': True,
        'msg': msg,
        'id': session.get('user_id'),
        'name': session.get('user_first_name') + ' ' + session.get('user_last_name'),
    }

    emit('send_Message', context, room=room_id)
    save_message(context, room_id, msg)


@socket_io.on('unique_wire', namespace='/chat')
def unique_wire(data):
    user = session.get('user_id')
    print('Create unique_wire for user ID:', user, data)
    join_room(user)


@socket_io.on('join_all_rooms', namespace='/chat')
def join_all_rooms(data):
    rooms = data.get('rooms')
    if rooms is not None:
        for x in rooms:
            if x:
                join_room(x)
                print('USER id :', session.get('user_id'), 'joining room : ' + x)


@socket_io.on('connect')
def connect_user():
    number_of_connecting, user_id = control_user_online(connect=True)
    connecting(number_of_connecting, user_id, conn=True)


@socket_io.on('disconnect')
def disconnect_user():
    number_of_connecting, user_id = control_user_online()
    connecting(number_of_connecting, user_id)
