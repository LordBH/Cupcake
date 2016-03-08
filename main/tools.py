def all_users_context(query, current_id):
    from models.models import ActivatedUsers

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
            # 'active': q.get('active'),
            'status': q.get('status'),
            'city': q.get('city'),
            'phone': q.get('phone'),
            'birthday': str(q.get('birthday')),
            'activated': a.activated

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


def loading_user(user_id):
    from models.models import User, datetime, session, db

    if session.get('user_active'):
        print(' - session - ')
        return User(reverse_user_session=True)

    print(' - request to DB - ')
    query = User.query.filter(User.id == user_id).first()

    if query is None:
        return None

    query.online = True
    query.active = datetime.now()
    user = User(query=query, user_session=True)

    db.session.commit()

    return user
