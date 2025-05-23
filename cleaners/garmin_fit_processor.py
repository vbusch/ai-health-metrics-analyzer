from garmin_fit_sdk import Decoder, Stream, Profile, FIT_EPOCH_S

import pandas as pd
import os
import datetime
from pprint import pprint


heart_rate_data = []
def mesg_listener(mesg_num, message):
    global last_known_timestamp

    if mesg_num == Profile['mesg_num']['MONITORING']:
        timestamp = None
        heart_rate = None
        for record in message:
            if record == 'timestamp' and message[record] is not None:
                timestamp = message[record]
                last_known_timestamp = timestamp  # Update last known timestamp
            elif record == 'timestamp_16' and message[record] is not None:
                timestamp_16 = message[record]
                timestamp = last_known_timestamp + datetime.timedelta(seconds=timestamp_16)
            elif record == 'heart_rate':
                heart_rate = message[record]

            if heart_rate is not None:
                heart_rate_data.append({'timestamp': timestamp, 'heart_rate': heart_rate})

def extract_activity_data(fit_file_path):
    stream = Stream.from_file(fit_file_path)
    decoder = Decoder(stream)

    messages, errors = decoder.read(mesg_listener = mesg_listener,
                                    convert_datetimes_to_dates = True,
                                    # expand_sub_fields = True,
                                    # merge_heart_rates = True,
                                    # expand_components = True,)
                                    )

    if len(errors) > 0:
        print(f"Something went wrong decoding the file: {errors}")
        return

    # print
    print(f" LENGTH: {len(heart_rate_data)}")
    return pd.DataFrame(heart_rate_data)


def extract_sleep_data(fit_file_path):
    stream = Stream.from_file(fit_file_path)
    decoder = Decoder(stream)
    messages, errors = decoder.read()

    sleep_data = []
    for record in messages:
        timestamp = record.get('timestamp')
        sleep_stage = record.get('sleep_stage') # Adjust key
        if timestamp is not None and sleep_stage is not None:
            sleep_data.append({'timestamp': timestamp, 'sleep_stage': sleep_stage})
    return pd.DataFrame(sleep_data)

def process_fit_files(directory_path):
    all_data = []
    for filename in os.listdir(directory_path):
        if filename.endswith('.fit'):
            file_path = os.path.join(directory_path, filename)
            if 'SLEEP_DATA' in filename:
                df = extract_sleep_data(file_path)
            else:
                df = extract_activity_data(file_path)
            if df is not None:
                print(f" Adding data from {len(df)}")
                all_data.append(df)
    return pd.concat(all_data, ignore_index=True) if all_data else None