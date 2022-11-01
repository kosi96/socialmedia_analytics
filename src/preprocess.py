import os.path

import csv
import glob
import json
import pandas as pd
import re

messages_schema = ['source', 'sender', 'timestamp', 'content']

base_instagram_path = 'data/raw/instagram/messages/inbox'
base_facebook_path = 'data/raw/facebook/messages/inbox'
base_whatsapp_path = 'data/raw/whatsapp'


def get_message_file_via_friend_username(source_dir, friend_username):
    if source_dir == base_whatsapp_path:
        file_path = list(glob.iglob(f'{source_dir}/{friend_username}*/*.txt'))
    else:
        file_path = list(glob.iglob(f'{source_dir}/{friend_username}_*/*.json'))

    if len(file_path) == 0:
        raise Exception(f'Messages from {friend_username} were not found in {source_dir}. Please check if they exists.')
    elif len(file_path) > 2:
        raise Exception(f'There are multiple message files from {friend_username} in {source_dir}. '
                        f'Please merge it into one file.')
    return file_path[0]


def change_encoding(series):
    encoded = series.apply(str).str.encode('latin1')
    return encoded.str.decode('utf-8')


def to_valid_date_time_format(timestamp):
    x = timestamp.split('/')
    day, month = x[1], x[0]
    if len(day) == 1:
        day = '0' + day
    if len(month) == 1:
        month = '0' + month
    return f'{month}/{day}/{x[2]}'


def get_unique_usernames(series_username, my_username, friend_username):
    participants = list(series_username.unique())
    if len(participants) != 2:
        raise Exception(f'Application currently supports up to 2 sender. Yet {len(participants)} were found!')

    match_0 = check_character_matching(my_username, participants[0])
    match_1 = check_character_matching(my_username, participants[1])
    match_2 = check_character_matching(friend_username, participants[0])
    match_3 = check_character_matching(friend_username, participants[1])

    # Highest match wins
    if max(match_0, match_3) > max(match_1, match_2):
        return {participants[0]: my_username, participants[1]: friend_username}
    else:
        return {participants[0]: friend_username, participants[1]: my_username}


def check_character_matching(string1, string2):
    total_cnt = 0
    for c in string1:
        total_cnt += string2.lower().count(c)
    return total_cnt


def instagram_data_to_intermediate_format(file_path,  my_username, friend_username):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        data = json.load(f)
        df = pd.json_normalize(data, 'messages')
        df['source'] = 'ig'
        df = df.loc[:, ['source', 'sender_name', 'timestamp_ms', 'content']]
        df.columns = messages_schema

        ## Get human readable content (č, š, ž)
        df = df.apply(change_encoding)

        ## Unify usernames
        unique_usernames = get_unique_usernames(df['sender'], my_username, friend_username)
        df.replace({'sender': unique_usernames}, inplace=True)

        ## String unix time to timestamp index
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

    ## TODO: Perhaps set timestamp as index??
    # df.set_index('timestamp', inplace=True)


def facebook_data_to_intermediate_format(file_path, my_username, friend_username):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        data = json.load(f)
        df = pd.json_normalize(data, 'messages')
        df['source'] = 'fb'
        df = df.loc[:, ['source', 'sender_name', 'timestamp_ms', 'content']]
        df.columns = messages_schema

        ## Get human readable content (č, š, ž)
        df = df.apply(change_encoding)

        ## Unify usernames
        unique_usernames = get_unique_usernames(df['sender'], my_username, friend_username)
        df.replace({'sender': unique_usernames}, inplace=True)

        ## String unix time to timestamp index
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df


def whatsapp_data_to_intermediate_format(file_path, my_username, friend_username):
    with open(file_path, 'r', encoding='utf8') as f:
        reader = csv.reader(f, delimiter='-')

        messages_list = []
        sender, timestamp, content = None, None, None
        tmp_row = ["user", "date", "content"]
        for row in reader:

            ## There are some empty rows
            if len(row) == 0:
                continue

            ## Received a new valid message (IF there is also a sender!)
            elif re.match(r"\d/\d\d/\d\d, \d\d:\d\d", row[0]):
                user_and_content_present = row[1].split(':', 1)

                if (len(user_and_content_present) == 2):
                    messages_list.append(['wa', sender, timestamp, content])

                    timestamp = row[0].rstrip()
                    sender = user_and_content_present[0].strip()
                    content = user_and_content_present[1].strip()

            ## Content continues in the next line
            elif len(row) == 1:
                content += row[0]

    df = pd.DataFrame(messages_list[1:], columns=messages_schema)

    ## Unify usernames
    unique_usernames = get_unique_usernames(df['sender'], my_username, friend_username)
    df.replace({'sender': unique_usernames}, inplace=True)

    df['timestamp'] = df['timestamp'].apply(to_valid_date_time_format)
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%m/%d/%y, %H:%M')

    return df


if __name__ == '__main__':
    ig, fb, wa = None, None, None
    if not os.path.isfile('config.json'):
        raise Exception("No config.json found in the root directory.")
    with open('config.json', 'r') as f:
        config = json.load(f)
        # TODO: verify valid config (mandatory fields)

    my_username, friend_username = config['my_username'], config['friend_username']

    ig = instagram_data_to_intermediate_format(get_message_file_via_friend_username(base_instagram_path, friend_username),
                                               my_username, friend_username)
    fb = facebook_data_to_intermediate_format(get_message_file_via_friend_username(base_facebook_path, friend_username),
                                              my_username, friend_username)
    wa = whatsapp_data_to_intermediate_format(get_message_file_via_friend_username(base_whatsapp_path, friend_username),
                                              my_username, friend_username)

    df = pd.concat([ig, fb, wa])
    df.to_pickle(f'data/processed/{my_username}_{friend_username}.pkl')
    # df = pd.read_pickle(f'data/processed/{my_username}_{friend_username}.pkl')
    print('PyCharm')
