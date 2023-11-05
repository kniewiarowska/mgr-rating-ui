import base64
from datetime import datetime

import matplotlib
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine

import config
from mi_band_ui.datamodel.models import db
from mi_band_ui.repository.util.data_util import clean_up_list
from mi_band_ui.service.data_preparation_service import DataPreparationService
from mi_band_ui.service.judge_page import JudgePreparationService
from mi_band_ui.service.page_service import PagePreparationService
from mi_band_ui.service.start_page_service import StartPageService

matplotlib.use('Agg')

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)
engine = create_engine(config.Config.SQLALCHEMY_DATABASE_URI)
preparation_service = DataPreparationService(engine)
page_service = PagePreparationService(engine)
start_page_service = StartPageService(engine)
judge_page = JudgePreparationService(engine)


@app.route('/index', methods=['GET', 'POST'])
def index():
    usernames = preparation_service.get_usernames_as_array()
    if request.method == 'POST':
        selected_used = request.form['user']

    return render_template('index.html', users=usernames)


@app.route('/', methods=['GET'])
def start():
    existing_judges = start_page_service.get_existing_judges()
    return render_template('start.html', judges=existing_judges)


@app.route('/panel', methods=['GET'])
def panel():
    username = request.args.get('user')
    active_hour = request.args.get('active_hour', default=None)
    date = request.args.get('date')
    chosen_date = datetime.strptime(date, "%Y-%m-%d")
    judge = request.args.get('judge')
    user = page_service.get_user(username)

    # hourly_stats = page_service.get_dates_without_rate_daily_page(judge, chosen_date, user.id)
    hourly_stats = page_service.get_hourly_stats_for_user_and_date(user.id, chosen_date)
    #hourly_stats_not_rated = page_service.get_dates_without_rate_daily_page(judge, chosen_date, user.id)

    available_hours = []  # TODO read only hours that are not rated
    rated_hours = []
    for stat in hourly_stats:
        hour = stat.hour
        available_hours.append(hour)


    daily_plot = page_service.get_daily_plot_for_user_and_date(user.id, chosen_date)
    daily_image = base64.b64encode(daily_plot).decode("utf-8")

    if (active_hour is None) & (len(available_hours) > 0):

        hourly_plot = hourly_stats[0].image
        hourly_image = base64.b64encode(hourly_plot).decode("utf-8")

        active = available_hours[0]
        left = available_hours[1:]

        last = False
        if len(available_hours) == 0:
            last = True

        return render_template('dailypanel.html', judge=judge, user=username, date=chosen_date,
                               active_hours=[active], hours_left=left, daily_plot=daily_image, hourly_plot=hourly_image,
                               last=last)

    elif active_hour is not None:
        # TODO check the last one
        last = False
        size = len(available_hours) - 1
        index = available_hours.index(int(active_hour)) + 1
        if index == size:
            last = True
        hourly_plot = hourly_stats[index].image
        hourly_image = base64.b64encode(hourly_plot).decode("utf-8")

        completed = available_hours[0:index]
        active = [available_hours[index]]

        if index == size:
            return render_template('dailypanel.html', judge=judge, user=username, date=chosen_date,
                                   completed_hours=completed,
                                   active_hours=active, daily_plot=daily_image, hourly_plot=hourly_image, last=last)

        left = available_hours[(index + 1):]
        return render_template('dailypanel.html', judge=judge, user=username, date=chosen_date,
                               completed_hours=completed,
                               active_hours=active,
                               hours_left=left, daily_plot=daily_image, hourly_plot=hourly_image, last=last)
    else:
        return redirect(url_for('judge', judge=judge))


@app.route('/judge', methods=['GET'])
def judge():
    specified_judge = request.args.get('judge')
    if specified_judge == '':
        specified_judge = request.args.get('custom_option')
    stats_to_judge = judge_page.get_dates_without_rate(specified_judge)
    return render_template('panel.html', judge=specified_judge, rows_to_judge=stats_to_judge)


@app.route('/rate', methods=['POST'])
def rate():
    user = request.args.get('user')
    date = request.args.get('date')
    active_hour = request.args.get('active_hour')
    given_rate = request.args.get('rate')
    judge = request.args.get('judge')
    last = request.args.get('last')

    page_service.save_judge_rate(user, date, active_hour, given_rate, judge)
    date = date.split(" ")[0]

    if last == 'True':
        return redirect(url_for('judge', judge=judge))
    else:
        return redirect(url_for('panel', user=user, date=date, active_hour=active_hour, judge=judge))


if __name__ == '__main__':
    app.run()
    preparation_service.prepare_data()
