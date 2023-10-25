from datetime import date

from mi_band_ui.plot.plot_generator import prepare_image
from mi_band_ui.repository.hourly_stats_repository import HourlyStatsRepository
from mi_band_ui.repository.miband_repository import MiBandRepository
from mi_band_ui.repository.user_repository import UserRepository
from mi_band_ui.repository.util.data_util import calculate_start_date, calculate_end_date, clean_up_data, clean_up_list
from mi_band_ui.statistic import statistics_calculator


class DataPreparationService:
    def __init__(self, engine):
        self.engine = engine
        self.userRepository = UserRepository(self.engine)
        self.miBandRepository = MiBandRepository(self.engine)
        self.hourlyStatsRepository = HourlyStatsRepository(self.engine)

    #TODO
    # def prepare_data(self):
        # get the list of user

        # for each user
            # get the list of available dates
            # check if data exists
            # if not: generate data

    #TODO
    # display particular data - that is requested

    def program_starts_for_user_and_day(self, username, day, month, year):
        df = self.get_cleaned_mi_band_data_for_day_and_user(username, day, month, year)
        user = self.userRepository.read_user(username)
        self.calculate_statistic_and_plot_for_whole_day(df, day, month, year, user)

    def get_cleaned_mi_band_data_for_day_and_user(self, username, day, month, year):
        start = calculate_start_date(day, month, year)
        end = calculate_end_date(day, month, year)

        df = self.miBandRepository.read_data_from_database_for_user_and_day(username, start, end)
        return clean_up_data(df)

    def calculate_statistic_and_plot_for_whole_day(self, df, day, month, year, user):
        data = {x: y for x, y in df.groupby(df['hour'])}
        for hour_df in data.items():
            image = prepare_image(hour_df, day, month, year)
            new_statistic = statistics_calculator.prepare_statistic_from_one_hour(hour_df[1], user, image,
                                                                                  hour_df[0],
                                                                                  date(year, month, day))
            self.hourlyStatsRepository.save_statistics(new_statistic)

    def get_usernames_to_drop_down(self):
        users = self.userRepository.get_usernames()
        return clean_up_list(users)
