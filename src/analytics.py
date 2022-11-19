import emoji as emoji
from collections import Counter
import pandas as pd

from preprocess import get_preprocessed_data_frame


def message_overall_frequency(df, period):
    return df.resample(period, closed='right', label='right').size()


def message_daily_frequency(df, period, username=None):
    if username is not None:
        tmp_df = df.loc[df['sender'] == username, :]
    else:
        tmp_df = df.copy()

    tmp_df = tmp_df.resample(period, closed='right', label='right').size()
    tmp_df = tmp_df.groupby(tmp_df.index.time).sum()

    # To get back datetime index
    tmp_df.index = pd.to_datetime(tmp_df.index, format='%H:%M:%S')
    return tmp_df


def favored_emojis_in_message(df, number, username):
    tmp_df = df.loc[df['sender'] == username, :]

    # Concatenate whole conversation in a string
    content = tmp_df['content'].str.cat(sep=' ')
    emojis = extract_emojis_from_string(content)

    most_common_emojis = Counter(emojis).most_common(number)

    # Normalize most common emojis
    normalize_most_common_emojis = []
    for pair in most_common_emojis:
        value = round(pair[1]/len(emojis) * 100, 1)
        normalize_most_common_emojis.append((pair[0], value))

    results = dict(reversed(normalize_most_common_emojis))
    return results


def extract_emojis_from_string(content):
    return [w for w in content if emoji.is_emoji(w)]


def message_response_time(df, working_hours_from, working_hours_to, my_username, friend_username):
    avg_response_time_in_min = {my_username: {}, friend_username: {}}

    for source, df_source in df.groupby('source'):
        # Take into the account only "awake" hours
        df_source = df_source.between_time(working_hours_from, working_hours_to)

        # Discard multiple messages that are usually sent at once
        df_source = df_source.loc[df_source['sender'] != df_source['sender'].shift(1), :]

        # Get seconds needed for each response
        df_source['response_time'] = df_source.index.to_series() - df_source.index.to_series().shift(1)
        df_source = df_source.dropna()
        df_source['response_time_s'] = df_source['response_time'].dt.total_seconds().astype(int)

        # Discard outliers, if response is longer than 1 day
        df_source = df_source.loc[df_source['response_time_s'] < 3600 * 24, :]

        results_tmp = df_source.loc[:, ['sender', 'response_time_s']].groupby('sender').mean().to_dict().get('response_time_s')

        avg_response_time_in_min[my_username][source] = int(results_tmp[my_username]/60)
        avg_response_time_in_min[friend_username][source] = int(results_tmp[friend_username]/60)

    return avg_response_time_in_min