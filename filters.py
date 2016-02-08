from datetime import datetime


def online(time):
    now = datetime.now()
    full_time = str(time.hour) + ':' + str(time.minute)
    full_date = str(time.day) + '.' + str(time.month) + '.' + str(time.year)

    if now.date() > time.date():
        if now.day == time.day + 1:
            return 'Last seen yesterday at ' + full_time

        return 'Last seen ' + full_date

    if now.hour - 3 > time.hour:
        return 'Last seen ' + str(now.hour - time.hour) + ' hours'
    elif now.hour > time.hour:
        return 'Last seen at ' + full_time

    if now.minute > time.minute:
        return 'Last seen ' + str(now.minute - time.minute) + ' min'

    return 'Last seen ' + str(now.second - time.second) + 'sec'


fil = (

    online,

)
