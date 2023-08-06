import os

from pandas import DataFrame

from ml_sdk.ml.sdk.watchmen.sdk import load_dataset_by_name, push_notebook_to_watchmen
from ml_sdk.ml.unitls import get_notebook, get_environment


class WatchmenClient(object):
    def __init__(self, token):
        if token:
            self.token = token
        else:
            self.token = os.environ.get('TOKEN')

    def load_dataset(self, name,dataframe_type="pandas"):
        return load_dataset_by_name(self.token, name,dataframe_type)

    def register_notebook(self, storage_type="file"):
        notebook = get_notebook(storage_type)
        notebook.environment = get_environment()
        response = push_notebook_to_watchmen(notebook,self.token)
        if response.status_code == 200:
            print("push notebook successfully")
        return notebook

    def save_topic_dataset(self, topic_name: str, dataset:DataFrame):
        pass


    def register_model(self):
        pass

#
# client  = WatchmenClient(token="0Z6ag50cdIPamBIgf8KfoQ")
# df = client.load_dataset("DEMO")
# print(df)
