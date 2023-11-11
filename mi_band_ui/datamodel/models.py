from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Date, BigInteger, LargeBinary, ForeignKeyConstraint, Float
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint

db = SQLAlchemy()


class FeelingResult(db.Model):
    __tablename__ = 'feeling_result'

    id = Column(BigInteger, primary_key=True, nullable=False)
    feeling_rate = Column(Integer, nullable=True)
    timestamp = Column(String(255), nullable=True)
    user_id = Column(String(255), nullable=True)


class MiBand(db.Model):
    __tablename__ = 'mi_band'

    id = Column(BigInteger, primary_key=True, nullable=False)
    device_id = Column(String(255), nullable=True)
    raw_kind = Column(String(255), nullable=True)
    raw_intensity = Column(String(255), nullable=True)
    steps = Column(String(255), nullable=True)
    timestamp = Column(String(255), nullable=True)
    user_id = Column(String(255), nullable=True)
    heart_rate = Column(String(255), nullable=False)


class Users(db.Model):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String(50), nullable=True)
    password = Column(String(120), nullable=True)
    username = Column(String(20), nullable=True)


class HourlyStatistic(db.Model):
    __tablename__ = 'hourly_statistic'

    id = Column(Integer, primary_key=True, autoincrement=True)
    steps = Column(Integer, nullable=False)
    heart_rate_avg = Column(Float, nullable=False)
    max_heart = Column(Integer, nullable=False)
    min_heart = Column(Float, nullable=False)
    raw_intensity_avg = Column(Float, nullable=False)
    time_of_day = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    hour = Column(Integer, nullable=False)
    user_id = Column(BigInteger, nullable=False)

    # Assuming 'User' is the related table with an 'id' field
    user = relationship('Users', foreign_keys=[user_id], lazy="joined")
    image = Column(LargeBinary, nullable=True)

    __table_args__ = (
        UniqueConstraint('hour', 'date', 'user_id', name='hourly_statistic_user_id_fk'),
        ForeignKeyConstraint(['user_id'], ['users.id'], name='hourly_statistic_user_id_fk')
    )


class Daily(db.Model):
    __tablename__ = 'daily'

    date = Column(Date, nullable=False)
    plot = Column(LargeBinary, nullable=False)
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False)

    # Assuming 'User' is the related table with an 'id' field
    user = relationship('Users', foreign_keys=[user_id], lazy="joined")

    # Define a unique constraint on the id column
    __table_args__ = (UniqueConstraint('id', name='daily_id_uindex'),
                      ForeignKeyConstraint(['user_id'], ['users.id'], name='daily_user_id_fk'))


class Rate(db.Model):
    __tablename__ = 'rate'

    id = Column(Integer, primary_key=True, autoincrement=True)
    judge = Column(String(50), nullable=False)
    hourly_stats_id = Column(Integer, nullable=False)
    rate = Column(Integer, nullable=True)

    hourly_statistic = relationship('HourlyStatistic', foreign_keys=[hourly_stats_id], lazy="joined")

    # Create a unique constraint for (judge, hourly_stats_id)
    __table_args__ = (UniqueConstraint('judge', 'hourly_stats_id', name='rate_pk'),
                      ForeignKeyConstraint(['hourly_stats_id'], ['hourly_statistic.id'],
                                           name='rate_hourly_statistic_id_fk'))

