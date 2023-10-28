
from sqlalchemy.orm import sessionmaker
from mi_band_ui.datamodel.models import User


class UserRepository:
    def __init__(self, engine):
        self.engine = engine

    def read_user(self, username=None):
        session = self.start_session()
        if username:
            query = session.query(User).filter(User.username == username)
            return query.first()
        self.end_session(session)
        return None

    def read_all(self):
        session = self.start_session()
        query = session.query(User)
        self.end_session(session)
        return query.all()

    def get_usernames(self):
        session = self.start_session()
        query = session.query(User.username)
        self.end_session(session)
        return query.all()

    def start_session(self):
        Session = sessionmaker(bind=self.engine)
        Session.expire_on_commit = False
        session = Session()
        return session

    def end_session(self, session):
        session.close()