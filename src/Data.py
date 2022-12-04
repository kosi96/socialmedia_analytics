import os

import pandas as pd

from preprocess import instagram_data_to_intermediate_format, facebook_data_to_intermediate_format, \
    get_message_file_via_friend_username, whatsapp_data_to_intermediate_format, BASE_INSTAGRAM_PATH, BASE_FACEBOOK_PATH, \
    BASE_WHATSAPP_PATH
from analytics import message_overall_frequency, message_daily_frequency, favored_emojis_in_message, \
    message_response_time
from pdf_generation import generate_pdf
from visualization import line_chart_with_moving_average, horizontal_bar_chart


class Data:
    def __init__(self, my_username, friend_username, my_custom_name, friend_custom_name):
        self.my_username = my_username
        self.friend_username = friend_username
        self.my_custom_name = my_custom_name
        self.friend_custom_name = friend_custom_name

        self.data_frame = None
        self.data_frame_file = f'data/processed/{self.my_username}_{self.friend_username}.pkl'
        self.pdf_file = f'pdf/{self.my_username}_{self.friend_username}.pdf'
        self.visualization_dir = f'data/visualization/{self.my_username}_{self.friend_username}/'

        self.__create_visualization_dir()

    def __create_visualization_dir(self):
        if not os.path.exists(self.visualization_dir):
            os.makedirs(self.visualization_dir)

    def fetch_data_frame(self):
        if os.path.isfile(self.data_frame_file):
            self.data_frame = pd.read_pickle(self.data_frame_file)

        else:
            ig = instagram_data_to_intermediate_format(
                get_message_file_via_friend_username(BASE_INSTAGRAM_PATH, self.friend_username),
                self.my_username, self.friend_username)

            fb = facebook_data_to_intermediate_format(
                get_message_file_via_friend_username(BASE_FACEBOOK_PATH, self.friend_username),
                self.my_username, self.friend_username)

            wa = whatsapp_data_to_intermediate_format(
                get_message_file_via_friend_username(BASE_WHATSAPP_PATH, self.friend_username),
                self.my_username, self.friend_username)

            df = pd.concat([ig, fb, wa])
            df.to_pickle(self.data_frame_file)
            self.data_frame = df

    def generate_message_overall_frequency_line_chart(self, period='1D', save=True):
        if save is True \
                and os.path.exists(self.visualization_dir + 'overall_freq.png'):
            return

        overall_freq = message_overall_frequency(self.data_frame, period=period)

        line_chart_with_moving_average(overall_freq,
                                       type='overall_freq',
                                       save=save,
                                       save_as=self.visualization_dir + 'overall_freq.png')
        # TODO: print/log that line chart is viewed/saved

    def generate_message_daily_frequency_line_chart(self, period='15min', save=True):
        if save is True \
                and os.path.exists(self.visualization_dir + 'daily_freq.png'):
            return

        daily_freq_overall = message_daily_frequency(self.data_frame, period=period)
        daily_freq_me = message_daily_frequency(self.data_frame, period=period, username=self.my_username)
        daily_freq_friend = message_daily_frequency(self.data_frame, period=period, username=self.friend_username)

        line_chart_with_moving_average(daily_freq_overall,
                                       type='day',
                                       series_ma=(daily_freq_me, daily_freq_friend),
                                       custom_name=(self.my_custom_name, self.friend_custom_name),
                                       save=True,
                                       save_as=self.visualization_dir + 'daily_freq.png')

    def generate_favored_emojis_bar_chart(self, number=5, save=True):
        if save is True \
                and os.path.exists(self.visualization_dir + 'favored_emojis_me.png') \
                and os.path.exists(self.visualization_dir + 'favored_emojis_friend.png'):
            return

        favored_emojis_me = favored_emojis_in_message(self.data_frame, number=number, username=self.my_username)
        favored_emojis_friend = favored_emojis_in_message(self.data_frame, number=number, username=self.friend_username)

        horizontal_bar_chart(favored_emojis_me,
                             title=f'Favored Emojis {self.my_custom_name}',
                             suffix=' %',
                             side='right',
                             save=save,
                             save_as=self.visualization_dir + 'favored_emojis_me.png')
        horizontal_bar_chart(favored_emojis_friend,
                             title=f'Favored Emojis {self.friend_custom_name}',
                             suffix=' %',
                             side='left',
                             save=save,
                             save_as=self.visualization_dir + 'favored_emojis_friend.png')

    def generate_response_time_bar_chart(self, save=True):
        if save is True \
                and os.path.exists(self.visualization_dir + 'response_time_me.png') \
                and os.path.exists(self.visualization_dir + 'response_time_friend.png'):
            return

        response_time = message_response_time(self.data_frame, working_hours_from='07:00', working_hours_to='23:00',
                                              my_username=self.my_username,
                                              friend_username=self.friend_username)

        horizontal_bar_chart(response_time[self.my_username],
                             title=f'Response time {self.my_custom_name}',
                             suffix=' min',
                             side='right',
                             save=save,
                             save_as=self.visualization_dir + 'response_time_me.png')
        horizontal_bar_chart(response_time[self.friend_username],
                             title=f'Response time {self.friend_custom_name}',
                             suffix=' min',
                             side='left',
                             save=save,
                             save_as=self.visualization_dir + 'response_time_friend.png')

    def generate_pdf(self):
        generate_pdf(self.pdf_file, self.visualization_dir, self.my_custom_name, self.friend_custom_name)

