from datamodel.models import db, Daily


class DailyRepository:
    def __init__(self, engine):
        self.engine = engine
        self.session = db.session

    def save_daily(self, new_daily):
        self.session.add(new_daily)
        self.session.commit()

    def get_daily_statistic(self, user_id, date):
        query = self.session.query(Daily).filter(Daily.date == date, Daily.user_id == user_id).first()
        return query.plot
