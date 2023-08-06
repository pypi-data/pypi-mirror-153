import json
from typing import List, Dict

import pandas as pd
import requests
from pandas import DataFrame

from ml_sdk.ml.model.factor_type import FactorType
from ml_sdk.ml.model.notebook import WatchmenNotebook

##TODO set url to env
from ml_sdk.ml.pd.untils import convert_to_pandas_type

local_env_url = "http://localhost:8000"


def build_headers(token):
    headers = {"Content-Type": "application/json"}
    headers["authorization"] = "pat " + token
    return headers


def build_indicators_and_types(columns):
    types = []
    indicators = []
    for column in columns:
        indicators.append({"columnId": column["columnId"], "name": column["alias"]})
        types.append({"columnId": column["columnId"], "name": column["alias"], "parameter": column["parameter"]})
    return indicators, types


def get_topic_ids(types):
    ids = []
    for column in types:
        parameter = column["parameter"]
        topic_id = parameter["topicId"]
        if topic_id not in ids:
            ids.append(topic_id)
    return ids


def load_topic_by_id(topic_ids: List, token):
    response = requests.post(local_env_url + "/topic/ids", data=json.dumps(topic_ids), headers=build_headers(token))
    topics = response.json()
    return topics


def convert_data_frame_type_by_types(data_frame: DataFrame, types: Dict[str, FactorType]) -> DataFrame:
    type_dict = {}
    for column in data_frame.columns:
        factor_type = types.get(column)
        if factor_type is not None:
            type_dict[column] = convert_to_pandas_type(factor_type)
        else:
            type_dict[column] = 'object'
    return data_frame.astype(type_dict)


def find_factor(topic_id, factor_id, topics):
    for topic in topics:
        if topic_id == topic["topicId"]:
            for factor in topic["factors"]:
                if factor_id == factor["factorId"]:
                    return factor



def build_columns_types(types, topics):
    columns_dict = {}

    for column in types:
        parameter = column["parameter"]
        topic_id = parameter["topicId"]
        factor_id = parameter["factorId"]
        factor = find_factor(topic_id, factor_id, topics)
        columns_dict[column["name"]] = FactorType(factor["type"])
    return columns_dict


def load_dataset_by_name(token, name, dataframe_type="pandas"):
    response = requests.get(local_env_url + "/subject/name", params={"name": name}, headers=build_headers(token))
    subject = response.json()
    indicators_list, types = build_indicators_and_types(subject["dataset"]["columns"])
    criteria = {
        "subjectId": subject["subjectId"],
        "indicators": indicators_list
    }

    topics = load_topic_by_id(get_topic_ids(types), token)
    columns_dict = build_columns_types(types, topics)

    response = requests.post(local_env_url + "/subject/data/criteria", data=json.dumps(criteria),
                             headers=build_headers(token))
    dataset = response.json()["data"]
    df =  pd.DataFrame(dataset, columns=list(map(lambda x: x["name"], indicators_list)))
    return convert_data_frame_type_by_types(df,columns_dict)


def push_notebook_to_watchmen(notebook: WatchmenNotebook, token):
    response = requests.post(local_env_url + "/notebook", data=notebook.json(),
                             headers=build_headers(token))
    return response


def save_data_to_topic(data_frame, topic_name, token):
    pass


df = load_dataset_by_name("WaRWTH5T-a3rxxqSvPtN6g", "customer_dataset")

print(df.dtypes)
