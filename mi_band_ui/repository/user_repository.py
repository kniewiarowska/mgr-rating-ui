
from sqlalchemy.orm import sessionmaker
from mi_band_ui.datamodel.models import User


class UserRepository:
    def __init__(self, engine):
        self.Session = sessionmaker(bind=engine)

    def read_user(self, username=None):
        with self.Session() as session:
            if username:
                query = session.query(User).filter(User.username == username)
            return query.first()

    def read_all(self):
        with self.Session() as session:
            query = session.query(User)
        return query.all()

    def get_usernames(self):
        with self.Session() as session:
            query = session.query(User.username)
        return query.all()
