from mi_band_ui.datamodel.models import Rate, HourlyStatistic
from mi_band_ui.repository.daily_repository import DailyRepository
from mi_band_ui.repository.hourly_stats_repository import HourlyStatsRepository
from mi_band_ui.repository.rate_repository import RateRepository


class JudgePreparationService:
    def __init__(self, engine):
        self.engine = engine
        self.hourlyStatsRepository = HourlyStatsRepository(self.engine)
        self.daily_repository = DailyRepository(self.engine)
        self.rate_repository = RateRepository(self.engine)

    def get_dates_without_rate(self, specified_judge):
        return self.hourlyStatsRepository.get_not_rated_statistics(specified_judge)
