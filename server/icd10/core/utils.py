import os
import re
from functools import wraps
from math import ceil
from typing import List, Tuple, Any
from model.custom_ner.extract_terms import extract_medical_terms
import pandas as pd
import scispacy
import spacy



def str2bool(value: str) -> bool:
    """ Parses string value and converts it to boolean """
    if isinstance(value, bool):
        return value
    elif value.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif value.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise ValueError('Boolean value expected')


def s3_url_to_bucket_name_keyword(s3_url):
    """
    Transforms s3_url to (bucket_name, keyword) pair.
    :param s3_url: str
    :return: (str, str). (bucket_name, keyword) pair
    """
    match = re.match('s3://([^/]*?)/(.*)', s3_url)
    if match:
        return match.group(1), match.group(2)
    else:
        return None, None


def get_url_type(file_url):
    """
    Returns the type (protocol) of a file url. Protocol can be s3, http, or local (local file).
    :param file_url: str
    :return: str
    """
    if re.match('s3://([^/]*?)/(.*)', file_url):
        return 's3'
    elif re.match('(http|https)://([^/]*?)/(.*)', file_url):
        return 'http'
    else:
        return 'local'


def get_extension(file_url):
    """
    Returns the extension of a file_url.
    :param file_url: str
    :return: str
    """
    if re.match('^.*\\.xls(x|m)?$', file_url):
        return 'excel'
    elif re.match('^.*\\.json$', file_url):
        return 'json'
    elif re.match('^.*\\.xml$', file_url):
        return 'xml'
    elif re.match('^.*\\.csv$', file_url):
        return 'csv'
    else:
        return None


def filepath_or_buffer_to_str(filepath_or_buffer, encoding="utf-8"):
    """
    Transforms filepath_or_buffer to str if filepath_or_buffer is a path or a buffer else returns it.
    :param filepath_or_buffer: Union[str, BytesIO]
    :param encoding: str
    :return: str
    """
    res = None
    try:
        filepath_or_buffer.seek(0)
        res = filepath_or_buffer.read().decode(encoding)
        retry = False
    except:
        retry = True

    if retry:
        try:
            res = open(filepath_or_buffer, "r", encoding=encoding).read()
            retry = False
        except:
            retry = True

    if retry:
        res = filepath_or_buffer
    return res


def split_df(df: pd.DataFrame, n_rows: int = 25) -> List[pd.DataFrame]:
    n_splits = ceil(len(df.index) / n_rows)
    split_starts = map(lambda idx: idx * n_rows, range(n_splits))
    return [
        df.iloc[i:min(i + n_rows, len(df.index)), :].copy().reset_index()
        for i in split_starts
    ]


def append_id(filename, id):
    return "{0}_{2}{1}".format(*os.path.splitext(filename) + (id,))


def map2starmap_adapter(func):
    """
    Function decorator to adapt func so that calling map on it behaves like starmap
    (not supported in threadpool executors)
    :param func: function
    :return: decorated function
    """

    @wraps(func)
    def func_wrapper(args: Tuple[Any], **kwargs):
        return func(*args, **kwargs)

    return func_wrapper


def get_medical_terms(text: str) -> List[str]:
    """
    Extracts medical terms from document
    """
    return extract_medical_terms(text)
