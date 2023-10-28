from sqlalchemy import text
from sqlalchemy.orm import sessionmaker


class HourlyStatsRepository:
    def __init__(self, engine):
        self.engine = engine

    def save_statistics(self, new_statistic):
        session = self.start_session()
        session.add(new_statistic)
        session.commit()
        self.end_session(session)

    def if_statistics_for_date_and_user_exist(self, user_id, date, hour=None):
        if hour is None:
            result = self.get_statistics_for_date_and_user(user_id, date)
        else:
            result = self.get_statistics_for_date_and_user_and_hour(user_id, date, hour)

        if result.count > 0:
            return True

        else:
            return False

    def get_statistics_for_date_and_user_and_hour(self, user_id, date, hour):

        query = text(
            "SELECT COUNT(*) as count " +
            "FROM db.hourly_statistic " +
            "WHERE user_id = :user_id AND date = :date AND hour = :hour"
        )

        params = {"user_id": user_id, "date": date, "hour": hour}
        session = self.start_session()
        result = session.execute(query, params).fetchone()
        self.end_session(session)
        return result

    def get_statistics_for_date_and_user(self, user_id, date):

        query = text(
            "SELECT COUNT(*) as count " +
            " FROM db.hourly_statistic " +
            " WHERE user_id = :user_id AND date = :date"
        )

        params = {"user_id": user_id, "date": date}
        session = self.start_session()
        result = session.execute(query, params).fetchone()
        self.end_session(session)
        return result

    def start_session(self):
        Session = sessionmaker(bind=self.engine)
        Session.expire_on_commit = False
        session = Session()
        return session

    def end_session(self, session):
        session.close()
