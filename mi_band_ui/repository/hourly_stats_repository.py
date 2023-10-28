from sqlalchemy import text

from mi_band_ui.datamodel.models import db


class HourlyStatsRepository:
    def __init__(self, engine):
        self.engine = engine
        self.session = db.session

    def save_statistics(self, new_statistic):
        self.session.add(new_statistic)
        self.session.commit()

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
        result = self.session.execute(query, params).fetchone()
        return result

    def get_statistics_for_date_and_user(self, user_id, date):

        query = text(
            "SELECT COUNT(*) as count " +
            " FROM db.hourly_statistic " +
            " WHERE user_id = :user_id AND date = :date"
        )

        params = {"user_id": user_id, "date": date}
        result = self.session.execute(query, params).fetchone()
        return result
