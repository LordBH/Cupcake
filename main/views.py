from flask import render_template, Blueprint
from models.models import Users


from_main = Blueprint('main', __name__, template_folder='templates',
                      static_folder='static', static_url_path='/%s' % __name__)


extra = from_main


@extra.route('/')
def index_page():
    Users.send_email('fugg@ukr.net')
    return render_template('base.html')
