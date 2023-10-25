from sqlalchemy.orm import sessionmaker

class HourlyStatsRepository:
    def __init__(self, engine):
        self.Session = sessionmaker(bind=engine)

    def save_statistics(self, new_statistic):
        with self.Session() as session:
            session.add(new_statistic)
            session.commit()
