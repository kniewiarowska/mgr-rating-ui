import base64
import logging

from flask import render_template

from mi_band_ui.datamodel.models import Rate
from mi_band_ui.repository.daily_repository import DailyRepository
from mi_band_ui.repository.hourly_stats_repository import HourlyStatsRepository
from mi_band_ui.repository.rate_repository import RateRepository
from mi_band_ui.repository.user_repository import UserRepository


class PagePreparationService:
    def __init__(self, engine):
        self.engine = engine
        self.userRepository = UserRepository(self.engine)
        self.hourlyStatsRepository = HourlyStatsRepository(self.engine)
        self.daily_repository = DailyRepository(self.engine)
        self.rateRepository = RateRepository(self.engine)

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

    def save_judge_rate(self, username, date, active_hour, rate_number, judge_name):
        user = self.get_user(username)
        hourly_statistics = self.hourlyStatsRepository.get_hourly_statistic_for_date_and_hour_and_user_id(active_hour,
                                                                                                          date, user.id)
        rate = Rate(judge=judge_name, hourly_stats_id=hourly_statistics.id, rate=rate_number)
        check_rate = self.rateRepository.get_rate(judge_name, hourly_statistics.id)
        if check_rate is None:
            self.rateRepository.save_rate(rate)
        else:
            print("Already judged")

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

    def get_dates_without_rate_daily_page(self, specifed_judge, date, user_id):
        return self.hourlyStatsRepository.get_not_rated_statistics_daily_page(specifed_judge, date, user_id)

    def get_dates_with_rate_daily_page(self, specifed_judge, date, user_id):
        return self.hourlyStatsRepository.get_rated_statistics_daily_page(specifed_judge, date, user_id)

    def make_page_for_first_run(self, hourly_stats_not_rated, hours_not_rated, judge, username,
                                chosen_date,
                                daily_image):

        for item in hourly_stats_not_rated:
            hours_not_rated.append(item.hour)

        hourly_plot = hourly_stats_not_rated[0].image
        hourly_image = base64.b64encode(hourly_plot).decode("utf-8")
        active = hours_not_rated[0]

        if len(hours_not_rated) == 1:  # jezeli tylko jeden rekord - zakoncz i nie ustawiaj tabli left i completed

            return render_template('dailypanel.html', judge=judge, user=username, date=chosen_date,
                                   active_hours=[active], daily_plot=daily_image,
                                   hourly_plot=hourly_image,
                                   last=True)

        else:  # jezeli wiecej niz jeden rekord zostal
            left = hours_not_rated[1:]
            return render_template('dailypanel.html', judge=judge, user=username, date=chosen_date,
                                   active_hours=[active], hour=active, hours_left=left, daily_plot=daily_image,
                                   hourly_plot=hourly_image,
                                   last=False)

    def make_page_for_rated_and_to_rate(self, hourly_stats_not_rated, hourly_stats_rated, judge, username,
                                        chosen_date,
                                        daily_image):
        hours_not_rated = []
        hours_rated = []

        for item in hourly_stats_not_rated:
            hours_not_rated.append(item.hour)

        for item in hourly_stats_rated:
            hours_rated.append(item.hour)

        hourly_plot = hourly_stats_not_rated[0].image
        hourly_image = base64.b64encode(hourly_plot).decode("utf-8")

        active = hours_not_rated[0]
        left = hours_not_rated[1:]
        completed = hours_rated

        return render_template('dailypanel.html', judge=judge, user=username, date=chosen_date,
                               active_hours=[active], hour=active, hours_left=left, completed_hours=completed,
                               daily_plot=daily_image,
                               hourly_plot=hourly_image,
                               last=False)

    def make_last_page(self, hourly_stats_not_rated, hourly_stats_rated, judge, username,
                       chosen_date,
                       daily_image):
        hours_not_rated = []
        hours_rated = []

        for item in hourly_stats_not_rated:
            hours_not_rated.append(item.hour)

        for item in hourly_stats_rated:
            hours_rated.append(item.hour)

        hourly_plot = hourly_stats_not_rated[0].image
        hourly_image = base64.b64encode(hourly_plot).decode("utf-8")

        active = hours_not_rated[0]
        completed = hours_rated

        return render_template('dailypanel.html', judge=judge, user=username, date=chosen_date,
                               active_hours=[active], hour=active, completed_hours=completed,
                               daily_plot=daily_image,
                               hourly_plot=hourly_image,
                               last=True)
