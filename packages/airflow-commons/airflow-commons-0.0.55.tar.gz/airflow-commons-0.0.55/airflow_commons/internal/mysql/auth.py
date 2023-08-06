from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_session(
    username: str,
    password: str,
    host: str,
    db_name: str = None,
):
    """

    :param username: database username
    :param password: database password
    :param host: database host
    :param db_name: database name
    :return:
    """
    db_connection_str = "mysql+pymysql://{username}:{password}@{host}/{dbname}".format(
        username=username, password=password, host=host, dbname=db_name
    )

    engine = create_engine(db_connection_str)
    session = sessionmaker(engine)

    return session
