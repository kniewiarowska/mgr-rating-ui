import base64
from datetime import datetime

import matplotlib
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine

import config
from mi_band_ui.datamodel.models import db
from mi_band_ui.service.data_preparation_service import DataPreparationService
from mi_band_ui.service.page_service import PagePreparationService

matplotlib.use('Agg')

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)
engine = create_engine(config.Config.SQLALCHEMY_DATABASE_URI)
preparation_service = DataPreparationService(engine)
page_service = PagePreparationService(engine)


@app.route('/index', methods=['GET', 'POST'])
def index():
    usernames = preparation_service.get_usernames_as_array()
    if request.method == 'POST':
        selected_used = request.form['user']

    return render_template('index.html', users=usernames)


@app.route('/bla', methods=['POST', 'GET'])
def bla():
    if request.method == 'POST':
        username = request.form['user']
        active_hour = None

    if request.method == 'GET':
        username = request.args.get('user')
        active_hour = request.args.get('active_hour', default=None)

    date = request.args.get('date')
    date = "2023-09-05"  #TODO change it
    judge = request.args.get('judge')  # TODO change it
    judge = "DUPA"

    chosen_date = datetime.strptime(date, "%Y-%m-%d")
    user = page_service.get_user(username)
    hourly_stats = page_service.get_hourly_stats_for_user_and_date(user.id, chosen_date)

    available_hours = [] #TODO read only hours that are not rated
    for stat in hourly_stats:
        hour = stat.hour
        available_hours.append(hour)

    daily_plot = page_service.get_daily_plot_for_user_and_date(user.id, chosen_date)
    daily_image = base64.b64encode(daily_plot).decode("utf-8")

    if (active_hour is None) & (len(available_hours) > 1):

        hourly_plot = hourly_stats[0].image
        hourly_image = base64.b64encode(hourly_plot).decode("utf-8")

        active = available_hours[0]
        left = available_hours[1:]
        last = False
        if len(available_hours) == 0:
            last = True

        return render_template('bla.html', judge=judge, user=username, date=chosen_date,
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
            return render_template('bla.html', judge=judge, user=username, date=chosen_date, completed_hours=completed,
                                   active_hours=active, daily_plot=daily_image, hourly_plot=hourly_image, last=last)

        left = available_hours[(index+1):]
        return render_template('bla.html', judge=judge, user=username, date=chosen_date, completed_hours=completed,
                               active_hours=active,
                               hours_left=left, daily_plot=daily_image, hourly_plot=hourly_image, last=last)
    else:
        print("a to chuj")


@app.route('/bla2', methods=['GET'])
def bla2():
    return render_template('index.html')


@app.route('/rate', methods=['POST'])
def rate():
    user = request.args.get('user')
    date = request.args.get('date')
    active_hour = request.args.get('active_hour')
    rate = request.args.get('rate')
    judge = request.args.get('judge')
    last = request.args.get('last')

    if last == 'True':
        return redirect(url_for('bla2', user=user, date=date, active_hour=active_hour, judge=judge))
    else:
        return redirect(url_for('bla', user=user, date=date, active_hour=active_hour, judge=judge))


if __name__ == '__main__':
    app.run()
    preparation_service.prepare_data()
