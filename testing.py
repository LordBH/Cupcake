from models.models import Users
from run_app import db


# admin = Users('admin', '123', 'example@admin.com')
# db.session.add(admin)
# db.session.commit()

y = Users.query.filter(Users.username == 'admin', Users.password == '123').all()

for x in y:
    print(x.__dict__)