from sqlite3 import IntegrityError

from datamodel.models import db, Rate


class RateRepository:
    def __init__(self, engine):
        self.engine = engine
        self.session = db.session

    def save_rate(self, new_rate):
        try:
            self.session.add(new_rate)
            self.session.commit()
        except IntegrityError as e:
            print(e)

    def get_daily_statistic(self):
        query = self.session.query(Rate)
        return query.all

    def get_judges_unique(self):
        return self.session.query(Rate.judge).distinct().all()

    def get_rate(self, specified_judge, hourly_stat_id):
        return self.session.query(Rate).filter(Rate.judge == specified_judge, Rate.hourly_stats_id == hourly_stat_id).first()
