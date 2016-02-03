from main.views import views_from_about
from registration.views import views_from_registration


blueprints = (

    views_from_about,
    views_from_registration,

    )
