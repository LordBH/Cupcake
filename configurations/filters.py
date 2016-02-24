from datetime import datetime
# from flask import session


def online(time):
    
    # print(session.get('user_id'), session.get('user_username'), session.get('user_email'),
    #       session.get('user_active'), session.get('user_online'), sep='\n')

    if time is None:
        return False

    now = datetime.now()
    full_time = str(time.hour) + ':' + str(time.minute if time.minute/10 > 1 else '0' + str(time.minute))
    full_date = str(time.day) + '.' + str(time.month) + '.' + str(time.year)

    if now.date() > time.date():
        if now.day == time.day + 1:
            return 'Last seen yesterday at ' + full_time

        return 'Last seen ' + full_date

    if now.hour - 3 > time.hour:
        return 'Last seen ' + str(now.hour - time.hour) + ' hours'
    elif now.hour > time.hour:
        return 'Last seen at ' + full_time + ' today'

    if now.minute > time.minute:
        return 'Last seen ' + str(now.minute - time.minute) + ' min'

    return 'Last seen ' + str(now.second - time.second) + 'sec'


filters = (

    online,

)
