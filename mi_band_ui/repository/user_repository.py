from mi_band_ui.datamodel.models import User, db


class UserRepository:
    def __init__(self, engine):
        self.engine = engine
        self.session = db.session

    def read_user(self, username=None):
        if username:
            query = self.session.query(User).filter(User.username == username)
            return query.first()
        return None

    def read_all(self):
        query = self.session.query(User)
        return query.all()

    def get_usernames(self):
        query = self.session.query(User.username)
        return query.all()
