"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User
import logging


logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """This method adds a new user to the database
        after taking the input of email and password
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """This algorithm would be used to search for users
        who have an account in the database
        """
        if not kwargs:
            raise InvalidRequestError("No filter criteria provided")
        try:
            return self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound("No user found matching the criteria.")
        except Exception as e:
            raise InvalidRequestError(str(e))

    def update_user(self, user_id: int, **kwargs) -> None:
        """This method, updates the user credentials after
        taking in the new parameters
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"Attribute '{key}' does not exist on User.")
            setattr(user, key, value)
        self._session.commit()
