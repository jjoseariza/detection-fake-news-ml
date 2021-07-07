import pandas
from io import StringIO
from config import config
from src.utils.blob_client import get_blob_container
from src.utils.logger import logging

class BlobLoader:
    def load_data(self):
        blob_container = get_blob_container(config["blob_loader"]["blob_container"])
        blob_list = blob_container.list_blobs(config["blob_loader"]["blob_file_prefix"])

        all_data = None
        for blob in blob_list:
            try:
                logging.info(f'Reading blob: {blob.name}')
                blob_client = blob_container.get_blob_client(blob.name)
                downloaded_blob = blob_client.download_blob()
                data = pandas.read_csv(StringIO(downloaded_blob.content_as_text()))
                logging.info(f'Size of {blob.name}: {data.size}')

                if all_data is None:
                    all_data = data
                all_data = all_data.append(data)
                logging.info(f'{blob.name} appends to all_data')
            except:
                logging.error(f'Error getting {blob.name}')

        return all_data