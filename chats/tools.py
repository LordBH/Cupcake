from flask import session, request


PEOPLE_ONLINE = {}


def compare(a, b):
    if a > b:
        return a, b
    else:
        return b, a


def change_online(user_id, online=True):
    from models.models import User, db
    q = User.query.filter_by(id=user_id).first()

    if online:
        q.online = True
    else:
        q.online = False

    db.session.add(q)
    db.session.commit()


def connecting(number, user, conn=False):
    ip = request.remote_addr
    if number is None:
        if conn:
            print('Anonymous user connect to CUPCAKE. His ip :', ip)
        else:
            print('Anonymous user disconnect from CUPCAKE. His ip :', ip)
        return

    if number == 0:
        change_online(user, False)
        return print("USER ID : |", user, '| disconnect from all pages on Cupcake. His ip :', ip)
    elif number == 1:
        change_online(user, True)
    print("USER ID : |", user, '| has', number, 'open page(s) on Cupcake. His ip :', ip)


def control_user_online(connect=False):
    id_ = session.get('user_id')

    if id_ is not None:
        PEOPLE_ONLINE.setdefault(id_, 0)
    else:
        return None, None

    if connect:
        PEOPLE_ONLINE[id_] += 1
    else:
        PEOPLE_ONLINE[id_] -= 1

    return PEOPLE_ONLINE[id_], id_


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


def save_message(context, room_id, msg):
    from models.models import Rooms, db, session

    a = room_id.split('|')
    user = session.get('user_id')

    if a[0] == str(user):
        q = Rooms(room_id, messages_1_=msg)
        context['id_user'] = a[0]
    else:
        q = Rooms(room_id, messages_2_=msg)
        context['id_user'] = a[1]

    db.session.add(q)
    db.session.commit()
