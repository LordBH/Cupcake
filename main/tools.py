from configurations.settings import ConfigClass
from os import path


def get_img(_id):
    u = str(_id)
    s = slash()
    file = ConfigClass.ABSOLUTE_IMAGES_FOLDER + s + u + '/' + u + '.jpg'
    static_path = ConfigClass.GET_IMAGE + s + u + '/' + u + '.jpg'

    if path.isfile(file):
        return static_path

    return ConfigClass.DEFAULT_IMG


def all_users_context(query, current_id):
    from models.models import ActivatedUsers, session

    data = {'people': []}

    for x in query:
        q = x.__dict__

        a = ActivatedUsers.query.filter_by(user_id=q.get('id')).first()
        extra = {
            'flag': True,
            'msg': 'success',
            'id': q.get('id'),
            'last_name': q.get('last_name'),
            'first_name': q.get('first_name'),
            'email': q.get('email'),
            'online': q.get('online'),
            'active': str(q.get('active')),
            'status': q.get('status'),
            'city': q.get('city'),
            'phone': q.get('phone'),
            'birthday': str(q.get('birthday')),
            'rooms': session.get('rooms'),
            'picture': get_img(q.get('id'))

        }

        if not extra.get('online'):
            """Re-write for active"""
            # extra['active'] = last_seen()
            pass

        if q.get('id') == current_id:
            for key, value in extra.items():
                data[key] = value
        else:
            data['people'].append(extra)

    return data


def get_rooms(user):
    from models.models import ActivatedUsers, session

    q = ActivatedUsers.query.filter_by(user_id=user).first()

    if q is None:
        from flask_login import redirect, url_for

        del session['user_active']
        return redirect(url_for('main.index_page'))

    if q.rooms is not None:

        arr = q.rooms.split('/')

        s = []

        for x in arr:
            if x:
                s.append(x)

        session['rooms'] = s


def loading_user(user_id):
    from models.models import User, datetime, session, db

    if session.get('user_active'):
        id_ = session.get('user_id')
        print(' --- LOGIN from sessions ---> ID :', id_)
        get_rooms(id_)
        return User(reverse_user_session=True)

    query = User.query.filter(User.id == user_id).first()

    if query is None:
        return None

    query.online = True
    query.active = datetime.now()
    user = User(query=query, user_session=True)
    print(' --- LOGIN with request to DB ---> ID :', user.id)

    db.session.commit()
    get_rooms(user.id)

    return user


def slash():
    from configurations.settings import ConfigClass

    extra = '/'
    if extra in ConfigClass.BASE_DIR:
        return extra
    return '\\'
