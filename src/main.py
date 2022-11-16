import os

from analytics import message_response_time, favored_emojis_in_message, message_overall_frequency, \
    message_daily_frequency, message_daily_frequency_per_user
from preprocess import load_config_file_and_fetch_usernames, get_preprocessed_data_frame
from visualization import horizontal_bar_chart, line_chart_with_moving_average


def create_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


if __name__ == '__main__':
    my_username, friend_username = load_config_file_and_fetch_usernames()
    dir = f'data/usecases/{my_username}_{friend_username}/'
    create_dir(dir)
    df = get_preprocessed_data_frame()

    '''
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


    # Fourth use-cae
    response_time = message_response_time(df, working_hours_from='07:00', working_hours_to='23:00',
                                          my_username=my_username,
                                          friend_username=friend_username)

    # line_chart_with_moving_average(overall_freq, type='year')

    # line_chart_with_moving_average(daily_freq_overall, [daily_freq_me, daily_freq_friend], type='day')

    # horizontal_bar_chart(favored_emojis_me, labels='left')
    # horizontal_bar_chart(favored_emojis_me, labels='right')

    horizontal_bar_chart(response_time[my_username], labels='left', save_as=dir + 'favored_emojis_me.png')
    horizontal_bar_chart(response_time[friend_username], labels='right', save_as=dir + 'favored_emojis_friend.png')

    print('PyCharm')
