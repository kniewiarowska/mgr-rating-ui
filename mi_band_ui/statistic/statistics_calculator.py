import math

from mi_band_ui.datamodel.models import HourlyStatistic


def calculate_heart_rate(item, heart_rate_mean):
    # remove wrong values
    heart_rate_data = item[((item['heart_rate'] > 38) & (item['heart_rate'] < 200))]  # remove wrong values

    # calculate average heart rate
    numer_of_heart_rate = (heart_rate_data.count()[0])
    if numer_of_heart_rate != 0:
        return heart_rate_data['heart_rate'].sum() / (heart_rate_data.count()[0])
    else:
        return heart_rate_mean


def max_heart_rate(item, heart_rate_mean):
    # remove wrong values
    heart_rate_data = item[((item['heart_rate'] > 38) & (item['heart_rate'] < 200))]  # remove wrong values
    maxv = heart_rate_data['heart_rate'].max()

    if math.isnan(maxv):
        return heart_rate_mean

    # calculate average heart rate
    return maxv


def min_heart_rate(item, heart_rate_mean):
    # remove wrong values
    heart_rate_data = item[((item['heart_rate'] > 38) & (item['heart_rate'] < 200))]  # remove wrong values

    # calculate average heart rate
    minv = heart_rate_data['heart_rate'].min()
    if math.isnan(minv):
        return heart_rate_mean

        # calculate average heart rate
    return minv


def calculate_raw_intensity(item, raw_intensity_mean):
    if item.count()[0] != 0:
        return item['raw_intensity'].sum() / (item.count()[0])
    else:
        return raw_intensity_mean


def calculate_heart_rate_mean(item):
    # remove wrong values
    heart_rate_data = item[((item['heart_rate'] > 39) & (item['heart_rate'] < 200))]
    heart_rate_mean =  heart_rate_data['heart_rate'].mean()
    if math.isnan(heart_rate_mean):
        return 80.0
    else:
        return heart_rate_mean


def calculate_raw_intensity_mean(item):
    return item['raw_intensity'].mean()


def prepare_statistic_from_one_hour(item, user, image_value, hour_value, date_value):
    heart_rate_mean = calculate_heart_rate_mean(item)
    raw_intensity_mean = calculate_raw_intensity_mean(item)

    # sum steps
    steps_value = item['steps'].sum()

    # calculate average heart rate
    heart_rate_avg_value = round(calculate_heart_rate(item, heart_rate_mean), 2)

    max_heart_value = round(max_heart_rate(item, heart_rate_mean), 2)

    min_heart_value = round(min_heart_rate(item, heart_rate_mean), 2)

    # calculate average raw intensity
    raw_intensity_avg_value = calculate_raw_intensity(item, raw_intensity_mean)

    time_of_day_value = get_time_of_day(hour_value)

    return HourlyStatistic(steps=int(steps_value),
                           heart_rate_avg=float(heart_rate_avg_value),
                           hour=hour_value,
                           max_heart=int(max_heart_value),
                           min_heart=int(min_heart_value),
                           raw_intensity_avg=float(raw_intensity_avg_value),
                           date=date_value,
                           time_of_day=time_of_day_value,
                           user=user,
                           image=image_value)


def get_time_of_day(hour):
    return (int(hour) % 24 + 4) // 4
