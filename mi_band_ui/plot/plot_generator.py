from io import BytesIO

import matplotlib.pyplot as plt


def prepare_plot(df_cleaned, day, month, year, hour=None):
    heart_rate = df_cleaned['heart_rate']
    x1 = df_cleaned['time']
    steps = df_cleaned['steps']

    fig, ax1 = plt.subplots()
    ax1.set_ylabel('Steps', fontsize=10)
    ax1.set_xlabel('Time', fontsize=10)
    ax1.bar(x1, height=steps, color='r')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Heart rate', fontsize=10)
    ax2.plot(x1, heart_rate, color='b')

    plt.xticks(x1[::80], rotation='vertical')
    plt.title(prepare_plt_title(day, month, year, hour))
    return save_matplotlib_as_bytes_io(plt)


def prepare_image(df, day, month, year):
    return prepare_plot(df[1], day, month, year, df[0]).read()


def prepare_plot_for_day(df, day, month, year):
    return prepare_plot(df, day, month, year).read()


def prepare_plt_title(day, month, year, hour):
    return str(day) + " " + str(month) + '' + str(year) + '' + str(hour)


def save_matplotlib_as_bytes_io(plot):
    buffer = BytesIO()
    plot.savefig(buffer, format='png')
    buffer.seek(0)
    plot.close()
    return buffer
