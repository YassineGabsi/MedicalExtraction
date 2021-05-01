import io
import re
from typing import Callable, Union, Tuple, Optional

import boto3
import pandas as pd
import sys

from icd10.core.exceptions import DataFrameUnreadError, FetchFunctionUnresolvedError, ReadFunctionUnresolvedError
from icd10.core.logging import logger
from icd10.core.utils import (
    s3_url_to_bucket_name_keyword,
    get_url_type, get_extension,
    filepath_or_buffer_to_str,
)
from medical_extraction.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

# TODO: running this from ipython won't retrieve the correct creds (needs to be called with django)
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)
default_encodings = ['utf-8', 'cp1252']


def read(read_func: Callable, filepath_or_buffer: Union[str, io.BytesIO], file_url: str) -> pd.DataFrame:
    """
    Reads DataFrame from filepath_or_buffer using read_func.It attempts to read using the default encodings
    and if all encodings fail, raises a DataFrameUnreadError.
    This function is used to avoid replicating the read algorithm and to decouple it from various reading functions
    applying the strategy design pattern.
    :param read_func: function
    :param filepath_or_buffer: Union[str, BytesIO]
    :param file_url: str
    :param read_func_kwargs: dict
    :return: DataFrame
    """
    e, tb = None, None
    for encoding in default_encodings:
        try:
            try:
                filepath_or_buffer.seek(0)
            except AttributeError:
                pass

            res = read_func(filepath_or_buffer, encoding=encoding)
            return res
        except UnicodeDecodeError as e:
            logger.warning("reading file {} using encoding {} failed".format(file_url, encoding))
        except Exception as exc:
            e = exc
            tb = sys.exc_info()[2]

    raise DataFrameUnreadError("Couldn't read dataframe from file {} : {}".format(file_url, e)) from e


def fetch_s3(file_url: str) -> Tuple[io.BytesIO, str]:
    """
    Fetches data from s3 url, puts it in a bytes buffer and returns it with the file url
    :param file_url: str
    :return: BytesIO, str
    """
    bucket_name, keyword = s3_url_to_bucket_name_keyword(file_url)
    response = s3_client.get_object(Bucket=bucket_name, Key=keyword)
    file = response["Body"].read()
    return io.BytesIO(file), file_url


def fetch_http(file_url: str) -> Tuple[bytes, str]:
    """
    Fetches data from a http endpoint and returns the data buffer with the file url
    :param file_url: str
    :return: bytes array, str
    """
    from urllib.request import urlopen
    response = urlopen(file_url)
    _buffer = response.read()
    return io.BytesIO(_buffer), file_url


def fetch(file_url: str) -> Tuple[str, str]:
    """
    Used to keep the same file url and delegate fetching to pandas methods which accept filepath_or_buffer
    parameters. Returns :file_url, file_url
    :param file_url: str
    :return: str, str
    """
    return file_url, file_url


url_type_fetch_func_map = {
    "s3": fetch_s3,
    "http": fetch_http,
    "https": fetch_http,
    "local": fetch
}


def read_csv(filepath_or_buffer: Union[str, io.BytesIO], encoding: str = "utf-8") -> pd.DataFrame:
    """
    Read function. Delegates reading from filepath_or_buffer to pandas.read_csv function.
    Reads DataFrame from csv.
    :param filepath_or_buffer: Union[str, BytesIO]
    :param encoding: str
    :return: DataFrame
    """
    return pd.read_csv(filepath_or_buffer, encoding=encoding)


def read_excel(filepath_or_buffer: Union[str, io.BytesIO], encoding: str = "utf-8") -> pd.DataFrame:
    """
    Read function. Delegates reading from filepath_or_buffer to pandas.read_xml function.
    Reads DataFrame from excel.
    :param filepath_or_buffer: Union[str, BytesIO]
    :param encoding: str
    :return: DataFrame
    """
    return pd.read_excel(filepath_or_buffer, encoding=encoding)


def read_json(
        filepath_or_buffer: Union[str, io.BytesIO],
        encoding: str = 'utf-8',
        orient: str = 'records',
        match_by: Optional[str] = None
    ):
    """
    Read function. Preprocesses filepath_or_buffer if match_by is not None and delegates reading from
    filepath_or_buffer to pandas.read_json function.
    Reads DataFrame from json. If match_by is not not, filepath_or_buffer is converted to str (fetched) and
    the regex pattern in match_by is matched and passed to pandas.read_json.
    :param filepath_or_buffer: Union[str, BytesIO]
    :param encoding: str, default 'utf-8'
    :param orient: Indication of expected JSON string format. Compatible JSON strings can be produced by
        DataFrame.to_json() with a corresponding orient value. The set of possible orients is:
        *'split' : dict like {index -> [index], columns -> [columns], data -> [values]}
        *'records' : list like [{column -> value}, ... , {column -> value}]
        *'index' : dict like {index -> {column -> value}}
        *'columns' : dict like {column -> {index -> value}}
        *'values' : just the values array
        See pandas.read_json's documentation for more info :
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_json.html
    :param match_by: str. Regex pattern to be matched
    :return: DataFrame
    """
    data = filepath_or_buffer
    if match_by:
        data = filepath_or_buffer_to_str(filepath_or_buffer, encoding=encoding)
        data = re.match(match_by, data, flags=re.DOTALL).group(1)

    return pd.read_json(data, orient=orient)


extension_read_func_map = {
    'excel': read_excel,
    'json': read_json,
    'csv': read_csv,
}


def generic_read(file_url: str, fetch_func: Callable = None, read_func: Callable = None) -> pd.DataFrame:
    """
    Attempts to resolve the appropriate read function and  fetch function if not specified, depending on the
    file url's protocol (http, s3 or local file) and extension. If the fetch function and read function are
    explicitly specified, the resolution step is skipped.
    If the fetch function and read function cannot be resolved, FetchFunctionUnresolvedError or
    ReadFunctionUnresolvedError are raised respectively.
    If resolution is successful, a DataFrame is read using the fetch function and the read function.
    This function is used to avoid replicating the resolution  algorithm and to decouple it from various
    read and fetch functions applying the strategy design pattern.
    :param file_url: str
    :param fetch_func: function
    :param read_func: function
    :return:
    """
    if not fetch_func:
        fetch_func = url_type_fetch_func_map.get(get_url_type(file_url))
    if not read_func:
        read_func = extension_read_func_map.get(get_extension(file_url))

    if not fetch_func:
        raise FetchFunctionUnresolvedError("Could not resolve fetch function from file_url : {}".format(file_url))
    if not read_func:
        raise ReadFunctionUnresolvedError("Could not resolve fetch function from file_url : {}".format(file_url))

    filepath_or_buffer, file_url = fetch_func(file_url)
    res = read(read_func, filepath_or_buffer, file_url)
    return res
