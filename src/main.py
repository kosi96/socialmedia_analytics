import os

from analytics import message_response_time, favored_emojis_in_message, message_overall_frequency, \
    message_daily_frequency
from preprocess import get_preprocessed_data_frame, load_config, \
    get_usernames, get_custom_names
from visualization import horizontal_bar_chart, line_chart_with_moving_average


def create_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


if __name__ == '__main__':
    config = load_config()
    my_username, friend_username = get_usernames(config)
    my_custom_name, friend_custom_name = get_custom_names(config)

    DIR = f'data/usecases/{my_username}_{friend_username}/'
    create_dir(DIR)
    df = get_preprocessed_data_frame()
    # TODO check nan in content (IG)!!
    # TODO add custom name to config file!

    # First use-case
    overall_freq = message_overall_frequency(df, period='1D')

    # Second use-case
    daily_freq_overall = message_daily_frequency(df, period='15min')
    daily_freq_me = message_daily_frequency(df, period='15min', username=my_username)
    daily_freq_friend = message_daily_frequency(df, period='15min', username=friend_username)

    # Third use-case
    favored_emojis_me = favored_emojis_in_message(df, number=5, username=my_username)
    favored_emojis_friend = favored_emojis_in_message(df, number=5, username=friend_username)

    # Fourth use-cae
    response_time = message_response_time(df, working_hours_from='07:00', working_hours_to='23:00',
                                          my_username=my_username,
                                          friend_username=friend_username)

    # --------------------------------------------------------------------------------------------

    line_chart_with_moving_average(overall_freq,
                                   type='year',
                                   save=False,
                                   save_as=DIR + 'overall_freq.png')

    line_chart_with_moving_average(daily_freq_overall,
                                   type='day',
                                   series_ma=(daily_freq_me, daily_freq_friend),
                                   custom_name=('Blaž', 'Nika'),
                                   save=False,
                                   save_as=DIR + 'daily_freq.png')

    horizontal_bar_chart(favored_emojis_me,
                         title=f'Favored Emojis {my_custom_name}',
                         suffix=' %',
                         side='left',
                         save=False,
                         save_as=DIR + 'favored_emojis_me.png')

    horizontal_bar_chart(favored_emojis_friend,
                         title=f'Favored Emojis {friend_custom_name}',
                         suffix=' %',
                         side='right',
                         save=False,
                         save_as=DIR + 'favored_emojis_friend.png')

    horizontal_bar_chart(response_time[my_username],
                         title=f'Response time {my_custom_name}',
                         suffix=' min',
                         side='left',
                         save=False,
                         save_as=DIR + 'response_time_me.png')

    horizontal_bar_chart(response_time[friend_username],
                         title=f'Response time {friend_custom_name}',
                         suffix=' min',
                         side='right',
                         save=False,
                         save_as=DIR + 'response_time_friend.png')

    print('PyCharm')
