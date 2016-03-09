from flask import session
from flask.ext.socketio import emit, join_room, leave_room
from .tools import compare, take_message, save_room
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

    if room_id not in session['rooms']:
        join_room(room_id)
        session['rooms'].append(room_id)
        emit('unique_wire', {'flag': True, 'id': user_2, 'user': user_1}, room=user_2)
        save_room(user_1, user_2, room=room_id)

    if session.setdefault('flag_for_joined', True):
        session['flag_for_joined'] = False

        chat = take_message(room_id, extra)

        context = {
            'flag': True,
            'room': room_id,
            'history': chat,
        }

        emit('status', context, room=room_id)


@socket_io.on('message', namespace='/chat')
def message(data):
    from models.models import Rooms, db

    room_id = data.get('room')
    if room_id is None:
        return emit('send_Message', {'flag': False, 'msg': 'room is empty'})

    a = room_id.split('|')
    user = session.get('user_id')
    msg = data.get('msg')

    context = {
        'flag': True,
        'msg': msg,
    }

    if a[0] == str(user):
        q = Rooms(room_id, user1_mes=msg)
        context['id_user'] = a[0]
    else:
        q = Rooms(room_id, user2_mes=msg)
        context['id_user'] = a[1]

    db.session.add(q)
    db.session.commit()

    return emit('send_Message', context, room=room_id)


@socket_io.on('unique_wire', namespace='/chat')
def unique_wire(data):
    user = session.get('user_id')
    join_room(user)


@socket_io.on('join_all_rooms', namespace='/chat')
def join_all_rooms(data):
    rooms = data.get('rooms')
    if rooms is not None:
        for x in rooms:
            if x:
                join_room(x)
                print('Join room : ' + x)


@socket_io.on('left', namespace='/chat')
def left(data):
    room_id = data.get('room_id')
    if room_id is None:
        return emit('status', {'flag': False, 'msg': 'room_id is empty'})

    leave_room(room_id)

    return emit('status', {'msg': data.get('first_name') + ' has left the room.'}, room=room_id)
