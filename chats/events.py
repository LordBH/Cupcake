from flask import session
from flask_login import current_user
from flask.ext.socketio import emit, join_room, leave_room
from . import socket_io

socketio = socket_io


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)

    from models.rooms import Rooms, db

    a = room.split('|')

    if a[0] == str(current_user.id):
        q = Rooms(room, user1_mes=message['msg'])
    else:
        q = Rooms(room, user2_mes=message['msg'])

    db.session.add(q)
    db.session.commit()


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)
