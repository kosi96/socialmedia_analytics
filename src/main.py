import os

from analytics import message_overall_frequency, message_daily_frequency, favored_emojis_in_message, \
    message_response_time
from pdf import generate_pdf
from preprocess import load_config, get_usernames, get_custom_names, get_sources, fetch_data_frame
from visualization import line_chart_with_moving_average, horizontal_bar_chart


def create_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

if __name__ == '__main__':
    config = load_config()
    my_username, friend_username = get_usernames(config)
    my_custom_name, friend_custom_name = get_custom_names(config)
    sources = get_sources(config)

    PROCESSED_DIR = f'data/processed/'
    VISUALIZATION_DIR = f'data/visualization/{my_username}_{friend_username}/'
    create_dir(PROCESSED_DIR)
    create_dir(VISUALIZATION_DIR)

    df = fetch_data_frame(PROCESSED_DIR, sources, my_username, friend_username)


    # First use-case
    overall_freq = message_overall_frequency(df, period='1D')

    line_chart_with_moving_average(overall_freq,
                                   type='overall_freq',
                                   series_ma=None,
                                   custom_ma_name=None,
                                   save_as=VISUALIZATION_DIR + 'overall_freq.png')
    # Second use-case
    daily_freq_overall = message_daily_frequency(df, period='15min')
    daily_freq_me = message_daily_frequency(df, period='15min', username=my_username)
    daily_freq_friend = message_daily_frequency(df, period='15min', username=friend_username)

    line_chart_with_moving_average(daily_freq_overall,
                                   type='day',
                                   series_ma=(daily_freq_me, daily_freq_friend),
                                   custom_ma_name=(my_custom_name, friend_custom_name),
                                   save_as=VISUALIZATION_DIR + 'daily_freq.png')
    # Third use-case
    favored_emojis_me = favored_emojis_in_message(df, number=5, username=my_username)
    favored_emojis_friend = favored_emojis_in_message(df, number=5, username=friend_username)

    horizontal_bar_chart(favored_emojis_me,
                         title=f'Favored Emojis {my_custom_name}',
                         suffix=' %',
                         side='right',
                         save_as=VISUALIZATION_DIR + 'favored_emojis_me.png')
    horizontal_bar_chart(favored_emojis_friend,
                         title=f'Favored Emojis {friend_custom_name}',
                         suffix=' %',
                         side='left',
                         save_as=VISUALIZATION_DIR + 'favored_emojis_friend.png')

    # Fourth use-case
    response_time = message_response_time(df, working_hours_from='07:00', working_hours_to='23:00',
                                          my_username=my_username,
                                          friend_username=friend_username)

    horizontal_bar_chart(response_time[my_username],
                         title=f'Response time {my_custom_name}',
                         suffix=' min',
                         side='right',
                         save_as=VISUALIZATION_DIR + 'response_time_me.png')
    horizontal_bar_chart(response_time[friend_username],
                         title=f'Response time {friend_custom_name}',
                         suffix=' min',
                         side='left',
                         save_as=VISUALIZATION_DIR + 'response_time_friend.png')

    # Generate pdf
    generate_pdf(VISUALIZATION_DIR, my_username, friend_username, my_custom_name, friend_custom_name)

    print('PDF Generated!')
