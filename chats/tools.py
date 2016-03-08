def compare(a, b):
    if a > b:
        return a, b
    else:
        return b, a


def take_message(room, l=None, number=10):
    from models.models import Rooms

    query = Rooms.query.filter_by(room_id=room).order_by('id').all()[-number:]

    if query is None:
        return False

    extra = {}

    for i, x in enumerate(query):
        extra[i] = {l[0]: x.messages_1_, l[1]: x.messages_2_, 'time': str(x.time)}

    return extra


def save_room(*args, room):
    from models.models import ActivatedUsers, db

    for x in args:
        u = ActivatedUsers.query.filter_by(user_id=x).first()
        if u is not None:
            if u.rooms is None:
                u.rooms = ''
            if room not in u.rooms:
                u.rooms += room + '/'
                db.session.add(u)
    db.session.commit()
