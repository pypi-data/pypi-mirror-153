from google.cloud import bigquery


def connect(service_account_file: str):
    """
    Connects to Bigquery client with given service account file.

    :param service_account_file: relative location of service account json
    :return: a Client object instance required for API requests
    """
    return bigquery.Client.from_service_account_json(service_account_file)
