import emoji as emoji
from collections import Counter

from preprocess import get_preprocessed_data_frame, load_config_file_and_fetch_usernames


def message_overall_frequency(df, period):
    return df.resample(period, closed='right', label='right').size()


def message_daily_frequency(df, period):
    tmp_df = df.resample(period, closed='right', label='right').size()
    return tmp_df.groupby(tmp_df.index.time).sum()


def message_daily_frequency_per_user(df, period, username):
    tmp_df = df.loc[df['sender'] == username, :].resample(period, closed='right', label='right').size()
    return tmp_df.groupby(tmp_df.index.time).sum()


def favored_emojis_in_message(df, number, username):
    tmp_df = df.loc[df['sender'] == username, :]

    # Concatenate whole conversation in a string
    content = tmp_df['content'].str.cat(sep=' ')
    emojis = extract_emojis_from_string(content)

    most_common_emojis = Counter(emojis).most_common(number)
    normalize_most_common_emojis = [(pair[0], pair[1]/len(emojis) * 100) for pair in most_common_emojis]
    results = dict(reversed(normalize_most_common_emojis))
    return results


def extract_emojis_from_string(content):
    return [w for w in content if emoji.is_emoji(w)]


def message_response_time(df, working_hours_from, working_hours_to, my_username, friend_username):
    avg_response_time_in_s = {my_username: {}, friend_username: {}}

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

        # TODO: Add quantile distribution for more accurate results
        results_tmp = df_source.loc[:, ['sender', 'response_time_s']].groupby('sender').mean().to_dict().get('response_time_s')

        avg_response_time_in_s[my_username][source] = int(results_tmp[my_username])
        avg_response_time_in_s[friend_username][source] = int(results_tmp[friend_username])

    return avg_response_time_in_s


if __name__ == '__main__':
    my_username, friend_username = load_config_file_and_fetch_usernames()
    df = get_preprocessed_data_frame()

    '''
    # First use-case
    overall_freq = message_overall_frequency(df, period='1D')

    # Second use-case
    daily_freq_overall = message_daily_frequency(df, period='15min')
    daily_freq_me = message_daily_frequency_per_user(df, period='15min', username=my_username)
    daily_freq_friend = message_daily_frequency_per_user(df, period='15min', username=friend_username)

    # Third use-case
    favored_emojis_me = favored_emojis_in_message(df, number=5, username=my_username)
    favored_emojis_friend = favored_emojis_in_message(df, number=5, username=friend_username)
    '''

    # Fourth use-cae
    response_time_me = message_response_time(df, working_hours_from='07:00', working_hours_to='23:00',
                                             my_username=my_username,
                                             friend_username=friend_username)

    print('PyCharm')