from mi_band_ui.repository.daily_repository import DailyRepository
from mi_band_ui.repository.hourly_stats_repository import HourlyStatsRepository
from mi_band_ui.repository.user_repository import UserRepository


class PagePreparationService:
    def __init__(self, engine):
        self.engine = engine
        self.userRepository = UserRepository(self.engine)
        self.hourlyStatsRepository = HourlyStatsRepository(self.engine)
        self.daily_repository = DailyRepository(self.engine)

    def get_daily_plot_for_user_and_date(self, user_id, date):
        result = self.daily_repository.get_daily_statistic(user_id, date)
        return result

    def get_daily_plot_for_user_and_date_and_hour(self, user_id, date, hour):
        result = self.hourlyStatsRepository.get_statistics_for_date_and_user_and_hour(user_id, date, hour)
        return result.plot

    def get_hourly_stats_for_user_and_date(self, user_id, date):
        return self.hourlyStatsRepository.get_all_hours_for_one_day(user_id, date)

    def get_user(self, username):
        return self.userRepository.read_user(username)

    def split_list_by_value(self, lst, value):
        sublists = []
        sublist = []

        for item in lst:
            sublist.append(item)
            if item == value:
                sublists.append(sublist)
                sublist = []

        if sublist:
            sublists.append(sublist)

        return sublists

