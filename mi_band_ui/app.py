import atexit
import base64
from datetime import datetime

import matplotlib
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from apscheduler.triggers.interval import IntervalTrigger

import config
from mi_band_ui.datamodel.models import db
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


def prepare():
    with app.app_context():
        preparation_service2 = DataPreparationService(engine)
        preparation_service2.prepare_data()
        print('JOB DONE')
        print(datetime.now())


scheduler = BackgroundScheduler()
scheduler.add_job(func=prepare, trigger="interval", seconds=3600)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())


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
    active_hour = request.args.get('active_hour', default=None)  # TODO delete
    date = request.args.get('date')
    chosen_date = datetime.strptime(date, "%Y-%m-%d")
    judge = request.args.get('judge')
    user = page_service.get_user(username)

    hourly_stats_not_rated = page_service.get_dates_without_rate_daily_page(judge, chosen_date, user.id)
    hourly_stats_rated = page_service.get_dates_with_rate_daily_page(judge, chosen_date, user.id)
    daily_plot = page_service.get_daily_plot_for_user_and_date(user.id, chosen_date)
    daily_image = base64.b64encode(daily_plot).decode("utf-8")

    # not judged yet
    if len(hourly_stats_rated) == 0:
        # first run
        if len(hourly_stats_not_rated) >= 1:  # sa dane do oceny
            return page_service.make_page_for_first_run(hourly_stats_not_rated, hourly_stats_rated, judge, username,
                                                        chosen_date, daily_image)
        else:
            return page_service.make_last_page(hourly_stats_not_rated, hourly_stats_rated, judge, username,
                                               chosen_date,
                                               daily_image)

    elif (len(hourly_stats_rated) > 0) & (len(hourly_stats_not_rated) >= 2):
        return page_service.make_page_for_rated_and_to_rate(hourly_stats_not_rated, hourly_stats_rated, judge, username,
                                                            chosen_date, daily_image)

    elif len(hourly_stats_not_rated) == 1:
        return page_service.make_last_page(hourly_stats_not_rated, hourly_stats_rated, judge, username,
                                           chosen_date,
                                           daily_image)
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
