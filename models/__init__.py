from uuid import UUID

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def is_valid_uuid(uuid_to_test, version=4):
    """
    Check if uuid_to_test is a valid UUID.

    Parameters
    ----------
    uuid_to_test : str, UUID
    version : {1, 2, 3, 4}

    Returns
    -------
    `True` if uuid_to_test is a valid UUID, otherwise `False`.

    Examples
    --------
    >>> is_valid_uuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a')
    True
    >>> is_valid_uuid('c9bf9e58')
    False
    """

    if isinstance(uuid_to_test, UUID):
        return True
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except ValueError:
        return False

    return True


from models import common_model, applicants, results
