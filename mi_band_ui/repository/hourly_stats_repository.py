from operator import and_

from sqlalchemy import text

from mi_band_ui.datamodel.models import db, HourlyStatistic, Rate


class HourlyStatsRepository:
    def __init__(self, engine):
        self.engine = engine
        self.session = db.session

    def save_statistics(self, new_statistic):
        self.session.add(new_statistic)
        self.session.commit()

    def update_hourly_stats(self, new_statistic, user_id, date, hour):
        record_to_update = self.get_hourly_statistic_for_date_and_hour_and_user_id(hour, date, user_id)
        if record_to_update:
            new_statistic.id = record_to_update.id
            self.session.merge(new_statistic)
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

    def get_hourly_statistic_for_date_and_hour(self, date, hour):
        query = self.session.query(HourlyStatistic).filter(HourlyStatistic.date == date, HourlyStatistic.hour == hour)
        return query.first()

    def get_hourly_statistic_for_date_and_hour_and_user_id(self, hour, date, user_id):
        query = self.session.query(HourlyStatistic).filter(HourlyStatistic.date == date, HourlyStatistic.hour == hour,
                                                           HourlyStatistic.user_id == user_id)
        return query.first()

    def get_all_hours_for_one_day(self, user_id, date):
        query = self.session.query(HourlyStatistic).filter(HourlyStatistic.date == date,
                                                           HourlyStatistic.user_id == user_id)
        return query.all()

    def get_not_rated_statistics(self, specifed_judge):
        query = text(
            "SELECT DISTINCT hs.date, u.username" +
            " FROM hourly_statistic hs" +
            " LEFT JOIN rate r ON hs.id = r.hourly_stats_id AND r.judge = :specifed_judge " +
            " LEFT JOIN user u ON hs.user_id = u.id " +
            " WHERE r.id IS NULL;")

        params = {"specifed_judge": specifed_judge}
        result = self.session.execute(query, params)

        return result.fetchall()

    def get_not_rated_statistics_daily_page(self, specifed_judge, date, user_id):
        query = text(
            "SELECT * FROM hourly_statistic hs LEFT JOIN rate r ON hs.id = r.hourly_stats_id AND " +
            "r.judge = :specifed_judge WHERE r.id IS NULL and hs.date = :date_value and hs.user_id = :user_id")

        params = {"specifed_judge": specifed_judge, 'date_value': date, 'user_id': user_id}
        result = self.session.execute(query, params)

        return result.fetchall()

    def get_rated_statistics_daily_page(self, specifed_judge, date, user_id):
        query = text(
            "SELECT * FROM hourly_statistic hs LEFT JOIN rate r ON hs.id = r.hourly_stats_id AND " +
            "r.judge = :specifed_judge WHERE r.id IS NOT NULL and hs.date = :date_value and hs.user_id = :user_id")

        params = {"specifed_judge": specifed_judge, 'date_value': date, 'user_id': user_id}
        result = self.session.execute(query, params)

        return result.fetchall()