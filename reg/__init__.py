from flask import Blueprint


from_reg = Blueprint('reg', __name__, template_folder='templates',
                     static_folder='static', static_url_path='/%s' % __name__)


from . import views
