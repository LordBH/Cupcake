from datetime import datetime
from time import sleep


def last_online(user, db):
    flag = False
    online = user.active
    now = datetime.now()
    if now.date() == online.date():
        online_min = online.hour * 60 + online.minute
        now_minute = now.hour * 60 + now.minute
        if now_minute - online_min < 15:
            return

    user.online = flag
    db.session.add(user)


def check_online(minutes=5, sec=60):
    from models.models import User, db

    while True:
        sleep(sec * minutes)
        q = User.query.all()
        for x in q:
            last_online(x, db)
        db.session.commit()
        print('Change online')
