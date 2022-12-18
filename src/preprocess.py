import os.path

import csv
import glob
import json
import pandas as pd
import re

messages_schema = ['source', 'sender', 'timestamp', 'content']

BASE_INSTAGRAM_PATH = 'data/raw/instagram/messages/inbox'
BASE_FACEBOOK_PATH = 'data/raw/facebook/messages/inbox'
BASE_WHATSAPP_PATH = 'data/raw/whatsapp'


def get_message_file_via_friend_username(source_dir, friend_username):
    if source_dir == BASE_WHATSAPP_PATH:
        file_path = list(glob.iglob(f'{source_dir}/{friend_username}_*/*.txt'))
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

        ## Fill nan content as it links to photos, reactinos, etc.
        df['content'] = df['content'].str.replace('nan', '[Not supported actions]')

        ## Unify usernames
        unique_usernames = get_unique_usernames(df['sender'], my_username, friend_username)
        df.replace({'sender': unique_usernames}, inplace=True)

        ## String unix time to timestamp index
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        df.sort_index(inplace=True)

    return df


def facebook_data_to_intermediate_format(file_path, my_username, friend_username):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        data = json.load(f)
        df = pd.json_normalize(data, 'messages')
        df['source'] = 'fb'
        df = df.loc[:, ['source', 'sender_name', 'timestamp_ms', 'content']]
        df.columns = messages_schema

        ## Get human readable content (č, š, ž)
        df = df.apply(change_encoding)

        ## Fill nan content as it links to photos, reactinos, etc.
        df['content'] = df['content'].str.replace('nan', '[Not supported actions]')

        ## Unify usernames
        unique_usernames = get_unique_usernames(df['sender'], my_username, friend_username)
        df.replace({'sender': unique_usernames}, inplace=True)

        ## String unix time to timestamp index
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        df.sort_index(inplace=True)

    return df


def whatsapp_data_to_intermediate_format(file_path, my_username, friend_username):
    with open(file_path, 'r', encoding='utf8') as f:
        reader = csv.reader(f, delimiter='-')

        messages_list = []
        sender, timestamp, content = None, None, None
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
    df.set_index('timestamp', inplace=True)
    df.sort_index(inplace=True)

    return df


def load_config():
    if not os.path.isfile('config.json'):
        raise Exception('No config.json found in the root directory.')

    with open('config.json', 'r') as f:
        config = json.load(f)

    # Check if there are mandatory keys in config.json
    for mandatory_key in ['my_username', 'friend_username', 'friend_username', 'my_custom_name', 'friend_custom_name']:
        if mandatory_key not in config.keys():
            raise Exception(f'Mandatory key: {mandatory_key} is not defined in config.json.')

    # Check valid sources in config.json
    valid_sources = ['whatsapp', 'instagram', 'facebook']
    for source in config['sources']:
        if source not in valid_sources:
            raise Exception(f'Invalid source: {source} defined in config.json. Currently supported sources are {*valid_sources,}.')

    return config


def get_usernames(config):
    return config['my_username'], config['friend_username']

def get_custom_names(config):
    return config['my_custom_name'], config['friend_custom_name']

def get_sources(config):
    return config['sources']

def fetch_data_frame(sources, my_username, friend_username):
    sources = '_'.join(sources)
    data_frame_file_name = f'data/processed/{my_username}_{friend_username}_{sources}.pkl'

    if os.path.isfile(data_frame_file_name):
        df = pd.read_pickle(data_frame_file_name)
        return df

    ig, fb, wa = None, None, None

    if 'instagram' in sources:
        ig = instagram_data_to_intermediate_format(
            get_message_file_via_friend_username(BASE_INSTAGRAM_PATH, friend_username),
            my_username, friend_username)

    if 'facebook' in sources:
        fb = facebook_data_to_intermediate_format(
            get_message_file_via_friend_username(BASE_FACEBOOK_PATH, friend_username),
            my_username, friend_username)

    if 'whatsapp' in sources:
        wa = whatsapp_data_to_intermediate_format(
            get_message_file_via_friend_username(BASE_WHATSAPP_PATH, friend_username),
            my_username, friend_username)

    df = pd.concat([ig, fb, wa])
    df.to_pickle(data_frame_file_name)
    return df
