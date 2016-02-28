from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from run_app import app, db
from models.models import User, ActivatedUsers
from models.chat import Rooms


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()

