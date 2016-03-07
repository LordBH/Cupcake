def compare(a, b):
    if a > b:
        return a, b
    else:
        return b, a


def take_message(room, number=10):
    from models.chat import Rooms

    q = Rooms.query.filter_by(room_id=room).order_by('id').all()[-number:]

    if q is None:
        return False

    return q
