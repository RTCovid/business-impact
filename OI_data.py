import os
from pathlib import Path
import pandas as pd
from datetime import datetime
from datetime import timedelta
import google_bq_helper_functions


def check_local_data_freshness():
    root_path = os.getcwd()
    OI_path = os.path.join(os.path.join(root_path, "data"), "Opportunity_Insights")

    timestamp_filename = "Opportunity_Insights_data_latest_download_timestamp.txt"
    timestamp_filepath_full = os.path.join(OI_path, timestamp_filename)

    if os.path.exists(timestamp_filepath_full):  # if .txt file exists
        with open(timestamp_filepath_full, 'r') as f:
            timestamp_str = f.read()

        timestamp_timestamp = datetime.strptime(timestamp_str, '%m/%d/%Y %H:%M:%S')
    else:
        timestamp_timestamp = None

    return timestamp_timestamp


def get_new_data_repo():
    """
    business-impact/                *(root_path / os.getcwd())*
    │
    ├── data/
        │
        ├── Opportunity_Insights/   *(OI_path)*
            │
            ├── Opportunity_Insights_data_latest_download_timestamp.txt
            ├── data/               *(OI_data_path)*
                │
                ├── Affinity - City - Daily.csv
                ├── Affinity - County - Daily.csv
                ├── ...
                ├── Zearn - State - Weekly.csv
    :return:
    """
    root_path = os.getcwd()
    OI_path = os.path.join(os.path.join(root_path, "data"), "Opportunity_Insights")
    # OI_data_path = os.path.join(OI_path, "data")

    try:
        Path(OI_path).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Error creating directory {OI_path} ({e})")

    os.chdir(OI_path)

    OI_repo_url = "https://github.com/Opportunitylab/EconomicTracker.git"
    try:
        os.system(f"svn export {OI_repo_url}/trunk/data --force")  # Reference: https://stackoverflow.com/a/40985185
    except Exception as e:
        print(f"Error downloading OI data ({e})")

    timestamp_filename = "Opportunity_Insights_data_latest_download_timestamp.txt"
    os.chdir(OI_path)
    with open(timestamp_filename, 'w') as log:
        log.write(f"{datetime.utcnow().strftime('%m/%d/%Y %H:%M:%S')}")

    os.chdir(root_path)


def parse_data(filename):
    if filename.endswith(".csv"):
        df = pd.read_csv(filename)
    elif filename.endswith(".txt"):
        # TODO: Read table/text
        df = pd.DataFrame()
        print(".txt file")
    else:
        # TODO: Read other
        df = pd.DataFrame()
        print("Other file extension (not csv or txt).")

    return df


def upload_new_data_gbq():
    # TODO: Upload new data to Google Big Query
    pass


def main(data_refresh_buffer_hrs=24):
    root_path = os.getcwd()
    OI_data_path = os.path.join(os.path.join(os.path.join(root_path, "data"), "Opportunity_Insights"), "data")

    timestamp_timestamp = check_local_data_freshness()
    if not timestamp_timestamp:  # If timestamp txt file doesn't exist
        print("No local data detected (no timestamp file -- Opportunity_Insights_data_latest_download_timestamp.txt)")
        get_new_data_repo()
    elif datetime.utcnow() - timestamp_timestamp >= timedelta(hours=data_refresh_buffer_hrs):  # If timestamp txt file exists and it has been over 24 hours since last data download
        print(f"More than 24 hours has elapsed since you last downloaded data (last download: {timestamp_timestamp} UTC); check for new data.")
        get_new_data_repo()
    elif datetime.utcnow() - timestamp_timestamp < timedelta(hours=data_refresh_buffer_hrs):  # If timestamp txt file exists and it has been under 24 hours since last data download
        print(f"Less than 24 hours has elapsed since you last downloaded data (last download: {timestamp_timestamp} UTC); use local data.")

        # for filename in os.listdir(OI_data_path):
        #     print("===================================================")
        #     # print(filename)
        #     df = parse_data(filename)
        #     print(df.head())
        #
        #     # TODO: Upload to GBQ? Create tables first, then append
        #     # TODO: Add all OI tables to gbq_creds
        #     # gbq_creds = google_bq_helper_functions.load_gbq_creds()
        #     # gbq_project_id = gbq_creds['project_id']
        #     # gbq_OI_table_id = gbq_creds[title]  # TODO: Reference table by title? Assumes OI doesn't change titles...
        #     #
        #     # google_bq_helper_functions.append_df_gbq(df, gbq_OI_table_id, gbq_project_id)


main()
