from flask import session, redirect, url_for, render_template, request
from . import from_chats
from flask_login import current_user


main = from_chats


@main.route('/im/<id_2>', methods=['GET', 'POST'])
def chat(id_2=None):
    # from models.models import User, db

    if current_user.is_authenticated:
        session['name'] = current_user.username

        # room_id_1 = '%d_%s' % (current_user.id, id_2)
        # room_id_2 = '%d_%s' % (id_2, current_user.id)
        #


        # session['room'] = '1'

        return redirect(url_for('.index'))
    return redirect(url_for('main.index_page'))


@main.route('/im', methods=['GET', 'POST'])
def index():
    # from chats.models.rooms import Rooms
    # from models.models import User

    return render_template('im.html', room='1')
