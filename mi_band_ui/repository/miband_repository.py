import pandas as pd

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


class MiBandRepository:
    def __init__(self, engine):
        self.engine = engine
        self.Session = sessionmaker(bind=engine)

    def read_data_from_database_for_user_and_day(self, user, start, end):
        query = text("SELECT CAST(steps as SIGNED) as steps,"
                     + " CAST(heart_rate as SIGNED) as heart_rate,"
                     + " CAST(raw_intensity as SIGNED) as raw_intensity,"
                     + " timestamp,"
                     + " CAST(HOUR(CONVERT_TZ(FROM_UNIXTIME(timestamp), 'UTC', 'Europe/Warsaw')) as SIGNED) as hour,"
                     + " CONCAT(LPAD(HOUR(CONVERT_TZ(FROM_UNIXTIME(timestamp), 'UTC', 'Europe/Warsaw')), 2, '0'), ':',"
                     + " LPAD(MINUTE(CONVERT_TZ(FROM_UNIXTIME(timestamp), 'UTC', 'Europe/Warsaw')), 2, '0')"
                     + " ) AS time"
                     + " FROM mi_band WHERE user_id = :user_name AND timestamp > :start AND timestamp < :end"
                     + " ORDER by timestamp")

        params = {"user_name": user, "start": start, "end": end}
        return pd.read_sql(query, self.engine, params=params)
