import os

from app import create_app
from flask_script import Manager
from flask_migrate import MigrateCommand

from config import config

env = os.environ.get("ENV", "development")
CONF = config[env]


app = create_app()
app.app_context().push()

manager = Manager(app)


@manager.command
def runtask(task_name):
    from workers import runtask

    with app.app_context():
        runtask(task_name)


if __name__ == "__main__":
    manager.add_command("db", MigrateCommand)
    manager.run()
