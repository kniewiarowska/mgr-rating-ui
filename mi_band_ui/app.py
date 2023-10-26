import matplotlib
from flask import Flask, render_template, request
from sqlalchemy import create_engine

import config
from mi_band_ui.datamodel.models import db
from mi_band_ui.service.data_preparation_service import DataPreparationService

matplotlib.use('Agg')

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)
engine = create_engine(config.Config.SQLALCHEMY_DATABASE_URI)

preparation_service = DataPreparationService(engine)


@app.route('/index', methods=['GET', 'POST'])
def index():
    selected_used = 'None'
    usernames = preparation_service.get_usernames_as_array()
    dic = preparation_service.bla()

    if request.method == 'POST':
        selected_used = request.form['user']

    if selected_used != 'None':
        preparation_service.program_starts_for_user_and_day(selected_used, 5, 9, 2023)

    # page_service.prepare_daily_plot(engine, selected_used, 5, 9, 2023)
    return render_template('index.html', img_path='static/img/daily_plot.png', users=usernames)

    # usernames = service.page_service.get_users(engine)
    # if request.method == 'POST':
    #     selected_used = request.form['user']
    #
    # if selected_used != 'None':
    #     service.page_service.prepare_daily_stuff(engine, selected_used, 5, 9, 2023)
    #     #page_service.prepare_daily_plot(engine, selected_used, 5, 9, 2023)
    #
    # return render_template('index.html', img_path='static/img/daily_plot.png', users=usernames)


if __name__ == '__main__':
    app.run()
