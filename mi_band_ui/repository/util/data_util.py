from datetime import datetime


def get_timestamp(day, month, year, hour, minute, seconds):
    date_with_time = datetime(year, month, day, hour, minute, seconds)
    return date_with_time.timestamp()


def calculate_start_date(day, month, year):
    return get_timestamp(day, month, year, 0, 0, 0)


def calculate_end_date(day, month, year):
    return get_timestamp(day, month, year, 23, 59, 59)


def clean_up_list(result):
    original_list = [list(row) for row in result]
    return [item for sublist in original_list for item in sublist]


def clean_up_data(df):
    start = df.index[df['time'] == '07:00'].tolist()[0]
    end = df.index[df['time'] == '22:00'].tolist()[0]

    df_cleaned = df.iloc[start:end]
    df_cleaned = df_cleaned[df_cleaned['heart_rate'] != 255]
    df_cleaned = df_cleaned.reset_index()
    return df_cleaned