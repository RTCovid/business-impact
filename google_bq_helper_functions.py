import os
import json
from google.cloud import bigquery
import pandas_gbq


def load_gbq_creds():
    cred_path = "RTC-business-impact-bd1c675235ef.json"
    if not os.path.isfile(cred_path):
        print('ERROR: No file called `creds.json` found in the path.')
        return None

    creds = json.load(open(cred_path,))
    return creds


def write_df_gbq_new_table(df, table_id, project_id):
    try:
        pandas_gbq.to_gbq(df, table_id, project_id, if_exists='replace')
        print(f"Successfully wrote DF to new BigQuery table (`{table_id}`)!")
    except Exception as e:
        print(f"Failed to write DF to new BigQuery table (`{table_id}`): {e}")


def append_df_gbq(df, table_id, project_id):
    try:
        pandas_gbq.to_gbq(df, table_id, project_id, if_exists='append')
        print(f"Successfully appended DF to new BigQuery table (`{table_id}`)!")
    except Exception as e:
        print(f"Failed to write DF to existing BigQuery table: {e}")


def read_gbq_df(sql, project_id):
    df = pandas_gbq.read_gbq(sql, project_id=project_id)
    return df



def load_csv_bq(filename, dataset_id, table_id):
    client = bigquery.Client()
    print(client)
    dataset_ref = client.dataset(dataset_id)  # TODO
    table_ref = dataset_ref.table(table_id)
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.skip_leading_rows = 1
    job_config.autodetect = True

    # with open(filename, "rb") as source_file:
    #     job = client.load_table_from_file(source_file, table_ref, job_config=job_config)
    #
    # job.result()  # Waits for table load to complete.
    #
    # print("Loaded {} rows into {}:{}.".format(job.output_rows, dataset_id, table_id))


def append_data_bq():
    # TODO
    pass

