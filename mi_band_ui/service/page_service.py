# import datamodel.models as model
# import plot
# import statistics
# import mgr-data-ui.repository.user_repository.
# from datetime import date
#
# # TODO rename
# def prepare_daily_stuff(engine, username, day, month, year):
#     # TODO: check if rows exists then:
#     df = app_repository.read_data_from_database_for_user_and_day(engine, username, day, month, year)
#     cleaned_df = clean_up_data(df)
#
#     #user_id = get_user_id(username, engine)
#     user = repository.read_user(username, engine)
#     bla_for_one_hour(cleaned_df, day, month, year, user, engine)
#
#     # if something missing calculate data
#
#     # safe plot for data
#
#
# # def prepare_daily_plot(engine, username, day, month, year):
# #     df = repository.read_data_from_database_for_user_and_day(engine, username, day, month, year)
# #     cleaned_df = clean_up_data(df)
# #     plot = plot_generator.wear_only_and_remove_values(cleaned_df, day, month, year, "")
# #     bla_for_one_hour(cleaned_df, day, month, year, plot)
#
#
# def clean_up_data(df):
#     start = df.index[df['time'] == '07:00'].tolist()[0]
#     end = df.index[df['time'] == '22:00'].tolist()[0]
#
#     df_cleaned = df.iloc[start:end]
#     df_cleaned = df_cleaned[df_cleaned['heart_rate'] != 255]
#     df_cleaned = df_cleaned.reset_index()
#     return df_cleaned
#
#
# def bla_for_one_hour(df, day, month, year, user_id, engine):
#     data = {x: y for x, y in df.groupby(df['hour'])}
#
#     for hour_df in data.items():
#         # TODO check if data exist before running
#         image = plot_generator.prepare_plot(hour_df[1], day, month, year, hour_df[0]).read()
#         new_statistic = statistics_calculator.prepare_statistic_from_one_hour(hour_df[1], user_id, image, hour_df[0],
#                                                                               date(year, month, day))
#         repository.save_statistics(engine, new_statistic)
#
#
# def get_users(engine):
#     result = repository.read_model_value(engine, model.User.username)
#     return clean_up_list(result)
#
#
# def get_user_id(username, engine):
#     return repository.read_user_id(engine, username)
#
#
# def clean_up_list(result):
#     original_list = [list(row) for row in result]
#     return [item for sublist in original_list for item in sublist]
