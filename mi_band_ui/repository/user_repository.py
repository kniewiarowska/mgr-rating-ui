from datamodel.models import Users, db


class UserRepository:
    def __init__(self, engine):
        self.engine = engine
        self.session = db.session

    def read_user(self, username=None):
        if username:
            query = self.session.query(Users).filter(Users.username == username)
            return query.first()
        return None

    def read_all(self):
        query = self.session.query(Users)
        return query.all()

    def get_usernames(self):
        query = self.session.query(Users.username)
        return query.all()
