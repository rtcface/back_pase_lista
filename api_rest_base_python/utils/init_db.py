from config.db_config import engine
from users.models.users_model import Users


def init_db():
    """
    Initializes the database
    :return:
    """
    # Create the database
    #engine.execute('CREATE DATABASE IF NOT EXISTS {}'.format(engine.url.database))



    # Create the tables
    Users.metadata.create_all(engine)
