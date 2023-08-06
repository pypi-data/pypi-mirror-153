import os
import json
import certifi
import pandas as pd
from datetime import datetime
from typing import Any, Generator
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionTimeout
from elasticsearch.helpers import parallel_bulk, bulk
from .. import decorator_manager


def index_json_bulk_parallel(index: str, method: str, **kwargs: Any) -> None:
    """
    Function index_json_bulk_parallel.
    Use this function to send data to elasticsearch with bulk indexing and multi-threading.

    Args:
        index(str): The name of index in elasticsearch.
        method (str): "json" send to elasticsearch with local .json file, or "dataframe" send to elasticsearch with pandas dataframe.
    Kwargs:
        keyword(str): Only for method="json", the keyword to filter json file. By default it is an empty string.
        json_path(str): Only for method="json", the local directory which contains json file.

        df(pd.Dataframe): Only for method="dataframe", pandas dataframe object to index.
    Examples:
        >>> from rcd_dev_kit import database_manager
        >>> database_manager.index_json_bulk_parallel(index="my_index", method="json", json_path="my_json_path", keyword="")
        >>> database_manager.index_json_bulk_parallel(index="my_index", method="dataframe", df=pd.DataFrame())
    """
    eo = ElasticsearchOperator(index=index)
    request_timeout = kwargs.get("request_timeout", 1200)
    if method == "json":
        eo.json_path = kwargs.get("json_path")
        eo.detect_json(keyword=kwargs.get("keyword"))
    elif method == "dataframe":
        eo.pd_dataframe = kwargs.get("df")
    else:
        raise ValueError(f"Unrecognized method: {method}")

    while True:
        try:
            eo.request_timeout = request_timeout
            eo.parallel_bulk_index()
            break
        except ConnectionTimeout:
            is_again = input(
                "Elasticsearch.exceptions.ConnectionTimeout Error... do you want to try again with request_timeout? (y or n)"
            )
            if is_again == "n":
                break
            while request_timeout <= 1200:
                request_timeout = int(
                    input("Enter your request_timeout setting: (integer > 1200)")
                )
            print(f"Restarting with time_out {request_timeout}.")


def index_json_bulk(
    json_path: str, index: str, keyword: str = "", **kwargs: Any
) -> None:
    """
    Function index_json_bulk.
    Use this function to send data to elasticsearch with bulk indexing.

    Args:
        json_path (str): The path of json directory.
        index(str): The name of index in elasticsearch.
        keyword(str): The keyword to filter json file. By default it is an empty string.
    Examples:
        >>> from rcd_dev_kit import database_manager
        >>> database_manager.index_json_bulk(index="my_index", json_path="my_json_path", keyword="")
    """
    eo = ElasticsearchOperator(index=index)
    eo.json_path = json_path
    eo.detect_json(keyword=keyword)
    request_timeout = kwargs.get("request_timeout", 1200)
    while True:
        try:
            eo.request_timeout = request_timeout
            eo.bulk_index()
            break
        except ConnectionTimeout:
            is_again = input(
                "Elasticsearch.exceptions.ConnectionTimeout Error... do you want to try again with request_timeout? (y or n)"
            )
            if is_again == "n":
                break
            while request_timeout <= 1200:
                request_timeout = int(
                    input("Enter your request_timeout setting: (integer > 1200)")
                )
            print(f"Restarting with time_out {request_timeout}.")


def index_json(
    json_path: str,
    index: str,
    keyword: str = "",
    show_debug: bool = True,
    **kwargs: Any,
):
    """
    Function index_json.
    Use this function to send data to elasticsearch with normal indexing.

    Parameters:
          json_path (str): The path of json directory.
          index(str): The name of index in elasticsearch.
          keyword(str): The keyword to filter json file. By default it is an empty string.
          show_debug(bool): Display debugging information or not.
    Examples:
        >>> from rcd_dev_kit import database_manager
        >>> database_manager.index_json(json_path="my_json_path", index="my_index", keyword="")
    """
    eo = ElasticsearchOperator(index=index)
    eo.json_path = json_path
    eo.detect_json(keyword=keyword)
    if kwargs.get("request_timeout"):
        eo.request_timeout = kwargs.get("request_timeout")
    eo.normal_index_json(show_debug=show_debug)


class ElasticsearchOperator:
    """
    Class ElasticsearchOperator.
    Use this class to manipulate data with elasticsearch.

    Parameters:
          index (str): elasticsearch index name.
    """

    def __init__(self, index: str) -> None:
        self.connection = Elasticsearch(
            hosts=os.environ.get("ELASTICSEARCH_HOST"),
            http_auth=(
                os.environ.get("ELASTICSEARCH_USER"),
                os.environ.get("ELASTICSEARCH_PASSWORD"),
            ),
            scheme=os.environ.get("ELASTICSEARCH_SCHEME"),
            port=os.environ.get("ELASTICSEARCH_PORT"),
            use_ssl=True,
            ca_certs=certifi.where(),
        )
        self._json_path = None
        self._pd_dataframe = None
        self._request_timeout = 1200
        self.index = index
        self.lst_json = list()

    @property
    def json_path(self) -> str:
        return self._json_path

    @json_path.setter
    def json_path(self, path: str) -> None:
        print(f"Setting json_path to {path}")
        self._json_path = path

    @property
    def pd_dataframe(self) -> pd.DataFrame:
        return self._pd_dataframe

    @pd_dataframe.setter
    def pd_dataframe(self, df: pd.DataFrame) -> None:
        print(f"Reading df with shape {df.shape}")
        self._pd_dataframe = df

    @property
    def request_timeout(self) -> int:
        return self._request_timeout

    @request_timeout.setter
    def request_timeout(self, value: int) -> None:
        print(f"Setting request_timeout to {value}")
        self._request_timeout = value

    def detect_json(self, keyword: str) -> None:
        self.lst_json = [
            file
            for file in os.listdir(self.json_path)
            if (file.endswith(".json"))
            and (not file.startswith("."))
            and (keyword in file)
        ]
        print(f"{len(self.lst_json)} .json files with keyword '{keyword}' detected.")

    def index_json(self, json_file: str, show_debug: bool = True) -> None:
        document_id = json_file.rsplit(".json")[0]
        with open(os.path.join(self.json_path, json_file)) as f:
            reader = json.load(f)
            reader["@timestamp"] = str(datetime.now())
            publish = self.connection.index(
                index=self.index,
                doc_type="_doc",
                id=document_id,
                body=reader,
                request_timeout=self._request_timeout,
            )
            if show_debug:
                print(f"Doc with id {publish['_id']} is published. ")

    @decorator_manager.timeit(program_name="Normal indexing")
    def normal_index_json(self, show_debug: bool = False) -> None:
        """
        Method normal_index_json, which calls self.index_json method.
        Use this method to index json data to elasticsearch.

        Parameters:
              show_debug (bool): Display debug information or not. By default it is True.
        """
        for json_file in self.lst_json:
            self.index_json(json_file=json_file, show_debug=show_debug)

    def json_generator(self) -> Generator:
        for json_file in self.lst_json:
            with open(os.path.join(self.json_path, json_file)) as f:
                d = json.load(f)
                d["@timestamp"] = str(datetime.now())
                yield {
                    "_id": json_file.split(".json")[0],
                    "_source": d,
                    "_index": self.index,
                }

    def df_generator(self) -> Generator:
        str_json = self.pd_dataframe.to_json(orient="records", force_ascii=False)
        lst_json = json.loads(str_json)
        for json_id, json_content in zip(self.pd_dataframe.index, lst_json):
            json_content["@timestamp"] = str(datetime.now())
            yield {"_id": json_id, "_source": json_content, "_index": self.index}

    def get_generator(self) -> Generator:
        if len(self.lst_json) != 0:
            print("Index by json files")
            return self.json_generator()
        elif not self.pd_dataframe.empty:
            print("Index by pandas dataframe")
            return self.df_generator()
        else:
            raise ValueError(
                f"Define at least one of the following: lst_json or pd_dataframe"
            )

    @decorator_manager.timeit(program_name="Bulk indexing")
    def bulk_index(self) -> None:
        bulk(
            client=self.connection,
            actions=self.get_generator(),
            request_timeout=self._request_timeout,
        )

    @decorator_manager.timeit(program_name="Parallel Bulk indexing")
    def parallel_bulk_index(self) -> None:
        for success, info in parallel_bulk(
            client=self.connection,
            actions=self.get_generator(),
            request_timeout=self._request_timeout,
        ):
            if not success:
                print(info)
