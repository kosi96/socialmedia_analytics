from src.analytics import message_response_time, favored_emojis_in_message, message_overall_frequency, \
    message_daily_frequency, message_daily_frequency_per_user
from src.preprocess import load_config_file_and_fetch_usernames, get_preprocessed_data_frame
from src.visualization import horizontal_bar_chart, line_chart_with_moving_average

if __name__ == '__main__':
    my_username, friend_username = load_config_file_and_fetch_usernames()
    df = get_preprocessed_data_frame()

    # First use-case
    overall_freq = message_overall_frequency(df, period='1D')

    # Second use-case
    daily_freq_overall = message_daily_frequency(df, period='15min')
    daily_freq_me = message_daily_frequency_per_user(df, period='15min', username=my_username)
    daily_freq_friend = message_daily_frequency_per_user(df, period='15min', username=friend_username)

    '''
    # Third use-case
    favored_emojis_me = favored_emojis_in_message(df, number=5, username=my_username)
    favored_emojis_friend = favored_emojis_in_message(df, number=5, username=friend_username)
    '''

    # horizontal_bar_chart(favored_emojis_me, labels='right')
    # line_chart_with_moving_average(overall_freq, type='year')
    line_chart_with_moving_average(daily_freq_overall, [daily_freq_me, daily_freq_friend], type='day')
    print('PyCharm')

