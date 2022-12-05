from src.Data import Data
from src.preprocess import load_config, get_usernames, get_custom_names, get_sources

if __name__ == '__main__':
    config = load_config()
    my_username, friend_username = get_usernames(config)
    my_custom_name, friend_custom_name = get_custom_names(config)
    sources = get_sources(config)

    data = Data(my_username, friend_username, my_custom_name, friend_custom_name, sources)
    data.fetch_data_frame()

    data.generate_message_overall_frequency_line_chart(period='1D')
    data.generate_message_daily_frequency_line_chart(period='15min')
    data.generate_favored_emojis_bar_chart(number=5)
    data.generate_response_time_bar_chart()

    data.generate_pdf()

    print('PyCharm')
