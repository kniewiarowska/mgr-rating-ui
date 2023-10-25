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


class User(db.Model):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String(50), nullable=True)
    password = Column(String(120), nullable=True)
    username = Column(String(20), nullable=True)


class HourlyStatistic(db.Model):
    __tablename__ = 'hourly_statistic'

    id = Column(Integer, primary_key=True, autoincrement=True)
    steps = Column(Integer, nullable=False)
    heart_rate_avg = Column(Float, nullable=True)
    max_heart = Column(Integer, nullable=True)
    min_heart = Column(Float, nullable=True)
    raw_intensity_avg = Column(Float, nullable=True)
    time_of_day = Column(Integer, nullable=True)
    date = Column(Date, nullable=True)
    hour = Column(Integer, nullable=True)
    user_id = Column(BigInteger, nullable=True)

    # Assuming 'User' is the related table with an 'id' field
    user = relationship('User', foreign_keys=[user_id])
    image = Column(LargeBinary, nullable=True)

    __table_args__ = (
        UniqueConstraint('hour', 'date', name='hourly_statistic_pk'),
        ForeignKeyConstraint(['user_id'], ['user.id'], name='hourly_statistic_user_id_fk')
    )
