import os
import json
from google.cloud import bigquery


def load_bq_creds():
    cred_path = "RTC-business-impact-bd1c675235ef.json"
    if not os.path.isfile(cred_path):
        print('ERROR: No file called `creds.json` found in the path.')
        return None

    creds = json.load(open(cred_path,))
    return creds


def load_csv_bq(filename, dataset_id, table_id):
    client = bigquery.Client()
    print(client)
    dataset_ref = client.dataset(dataset_id)
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

