from flask import Blueprint, render_template

views_from_about = Blueprint('main', __name__, template_folder='templates',
                             static_folder='static', static_url_path='/%s' % __name__)
extra = views_from_about


@extra.route('/')
def index_page():
    return render_template('about/index.html')
