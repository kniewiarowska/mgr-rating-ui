# from datetime import datetime
#
# import pandas as pd
# from sqlalchemy import text
# from sqlalchemy.orm import sessionmaker
#
#
# def read_model_value(engine, model_value):
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     query = session.query(model_value)
#     return query.all()
#
#
# def save_statistics(engine, new_statistic):
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     session.add(new_statistic)
#     session.commit()
#
#
# def read_data_from_database_for_user_and_day(engine, user, day, month, year):
#     query = text("SELECT CAST(steps as SIGNED) as steps,"
#                  + " CAST(heart_rate as SIGNED) as heart_rate,"
#                  + " CAST(raw_intensity as SIGNED) as raw_intensity,"
#                  + " timestamp,"
#                  + " CAST(HOUR(CONVERT_TZ(FROM_UNIXTIME(timestamp), 'UTC', 'Europe/Warsaw')) as SIGNED) as hour,"
#                  + " CONCAT(LPAD(HOUR(CONVERT_TZ(FROM_UNIXTIME(timestamp), 'UTC', 'Europe/Warsaw')), 2, '0'), ':',"
#                  + " LPAD(MINUTE(CONVERT_TZ(FROM_UNIXTIME(timestamp), 'UTC', 'Europe/Warsaw')), 2, '0')"
#                  + " ) AS time"
#                  + " FROM mi_band WHERE user_id = :user_name AND timestamp > :start AND timestamp < :end"
#                  + " ORDER by timestamp")
#
#     start = calculate_start_date(day, month, year)
#     end = calculate_end_date(day, month, year)
#
#     params = {"user_name": user, "start": start, "end": end}
#     return pd.read_sql(query, engine, params=params)
#
#
