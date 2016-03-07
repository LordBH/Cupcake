def compare(a, b):
    if a > b:
        return a, b
    else:
        return b, a


def take_message(room, l=None, number=10):
    from models.chat import Rooms

    query = Rooms.query.filter_by(room_id=room).order_by('id').all()[-number:]

    print(query[0].time)

    if query is None:
        return False

    extra = {}

    for i, x in enumerate(query):
        extra[i] = {l[0]: x.messages_1_, l[1]: x.messages_2_, 'time': x.time}

    return extra
