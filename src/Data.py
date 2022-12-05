import os

import pandas as pd
from fpdf import FPDF

from preprocess import instagram_data_to_intermediate_format, facebook_data_to_intermediate_format, \
    get_message_file_via_friend_username, whatsapp_data_to_intermediate_format, BASE_INSTAGRAM_PATH, BASE_FACEBOOK_PATH, \
    BASE_WHATSAPP_PATH
from analytics import message_overall_frequency, message_daily_frequency, favored_emojis_in_message, \
    message_response_time
from visualization import line_chart_with_moving_average, horizontal_bar_chart


class Data:
    def __init__(self, my_username, friend_username, my_custom_name, friend_custom_name, sources):
        self.my_username = my_username
        self.friend_username = friend_username
        self.my_custom_name = my_custom_name
        self.friend_custom_name = friend_custom_name
        self.sources = sources

        self.data_frame = None
        self.data_frame_file_name = None
        self.pdf_file = f'pdf/{self.my_username}_{self.friend_username}.pdf'
        self.visualization_dir = f'data/visualization/{self.my_username}_{self.friend_username}'

        self.__create_dir(self.visualization_dir)

    def __create_dir(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)

    def __get_processed_file_name(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)

    def fetch_data_frame(self):
        sources = '_'.join(self.sources)
        self.data_frame_file_name = f'data/processed/{self.my_username}_{self.friend_username}_{sources}.pkl'

        if os.path.isfile(self.data_frame_file_name):
            self.data_frame = pd.read_pickle(self.data_frame_file_name)
            return

        ig, fb, wa = None, None, None

        if 'instagram' in sources:
            ig = instagram_data_to_intermediate_format(
                get_message_file_via_friend_username(BASE_INSTAGRAM_PATH, self.friend_username),
                self.my_username, self.friend_username)

        if 'facebook' in sources:
            fb = facebook_data_to_intermediate_format(
                get_message_file_via_friend_username(BASE_FACEBOOK_PATH, self.friend_username),
                self.my_username, self.friend_username)

        if 'whatsapp' in sources:
            wa = whatsapp_data_to_intermediate_format(
                get_message_file_via_friend_username(BASE_WHATSAPP_PATH, self.friend_username),
                self.my_username, self.friend_username)

        df = pd.concat([ig, fb, wa])
        df.to_pickle(self.data_frame_file_name)
        self.data_frame = df

    def generate_message_overall_frequency_line_chart(self, period='1D'):
        overall_freq = message_overall_frequency(self.data_frame, period=period)

        line_chart_with_moving_average(overall_freq,
                                       type='overall_freq',
                                       series_ma=None,
                                       custom_ma_name=None,
                                       save_as=self.visualization_dir + '/overall_freq.png')

    def generate_message_daily_frequency_line_chart(self, period='15min'):
        daily_freq_overall = message_daily_frequency(self.data_frame, period=period)
        daily_freq_me = message_daily_frequency(self.data_frame, period=period, username=self.my_username)
        daily_freq_friend = message_daily_frequency(self.data_frame, period=period, username=self.friend_username)

        line_chart_with_moving_average(daily_freq_overall,
                                       type='day',
                                       series_ma=(daily_freq_me, daily_freq_friend),
                                       custom_ma_name=(self.my_custom_name, self.friend_custom_name),
                                       save_as=self.visualization_dir + '/daily_freq.png')

    def generate_favored_emojis_bar_chart(self, number=5):
        favored_emojis_me = favored_emojis_in_message(self.data_frame, number=number, username=self.my_username)
        favored_emojis_friend = favored_emojis_in_message(self.data_frame, number=number, username=self.friend_username)

        horizontal_bar_chart(favored_emojis_me,
                             title=f'Favored Emojis {self.my_custom_name}',
                             suffix=' %',
                             side='right',
                             save_as=self.visualization_dir + '/favored_emojis_me.png')
        horizontal_bar_chart(favored_emojis_friend,
                             title=f'Favored Emojis {self.friend_custom_name}',
                             suffix=' %',
                             side='left',
                             save_as=self.visualization_dir + '/favored_emojis_friend.png')

    def generate_response_time_bar_chart(self):
        response_time = message_response_time(self.data_frame, working_hours_from='07:00', working_hours_to='23:00',
                                              my_username=self.my_username,
                                              friend_username=self.friend_username)

        horizontal_bar_chart(response_time[self.my_username],
                             title=f'Response time {self.my_custom_name}',
                             suffix=' min',
                             side='right',
                             save_as=self.visualization_dir + '/response_time_me.png')
        horizontal_bar_chart(response_time[self.friend_username],
                             title=f'Response time {self.friend_custom_name}',
                             suffix=' min',
                             side='left',
                             save_as=self.visualization_dir + '/response_time_friend.png')

    def generate_pdf(self):
        CHARTS = {
            'overall_freq': (5, 30, 200, 90),

            'favored_emojis_me': (5, 130, 55, 60),
            'favored_emojis_friend': (55, 130, 55, 60),

            'response_time_me': (110, 130, 55, 60),
            'response_time_friend': (150, 130, 55, 60),

            'daily_freq': (5, 200, 200, 90),
        }

        pdf = FPDF()
        pdf.set_font('Arial', 'B', 16)
        pdf.set_text_color(245, 245, 245)
        pdf.set_draw_color(245, 245, 245)
        pdf.add_page()

        # Background
        pdf.image('data/visualization/BACKGROUND/bg_23272C.png', 0, 0, 210, 297)

        # Image
        pdf.cell(190, 10, f'{self.my_custom_name} vs {self.friend_custom_name}', 1, 0, 'C')

        for image_name, shape in CHARTS.items():
            image_path = f'{self.visualization_dir}{image_name}.png'
            x, y, w, h = shape
            pdf.image(image_path, x, y, w, h)

        pdf.line(5, 120, 205, 120)
        pdf.line(5, 190, 205, 190)
        pdf.output(self.pdf_file, "F")

