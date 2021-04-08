from django.core.files.uploadedfile import TemporaryUploadedFile
import pandas as pd
from io import StringIO
import numpy as np
import pandas.api.types as ptypes

COLUMNS = [
    "Title",
    "Research Summary",
    "Inclusion Criteria",
]

MAX_SIZE = 1024*1024*25

EXTENSIONS = {
    "csv": pd.read_csv, 
    **{
        key: pd.read_excel
        for key in ["xls", "xlsx", "xlsm", "xlsb", "odf", "ods", "odt"]
    }
}

def validate(file_obj: TemporaryUploadedFile):
    file_extension = next(iter([
        extension for extension in EXTENSIONS.keys() if
        file_obj.name.endswith(f".{extension}")
    ]), None)

    if not file_extension:
        return {
            "valid": False,
            "error": "Please upload a csv or excel file"
        }

    try:
        reader = EXTENSIONS[file_extension]
        df = reader(StringIO(file_obj.read().decode('utf-8')))
    except UnicodeDecodeError as e:
        print(e)
        return {
            "valid": False,
            "error": "Please use utf-8 encoding"
        }
    except:
        raise
    
    diff = list(np.setdiff1d(COLUMNS, list(df.columns)))
    if diff:
        return {
            "valid": False,
            "error": f"Columns {', '.join(diff)} do not exist in the dataset"
        }
    
    if file_obj.size > MAX_SIZE:
        return {
            "valid": False,
            "error": f"File size ({file_obj.size/(1024*1024)} MB) exceeded " \
                f"the maximum allowed file size ({MAX_SIZE/(1024*1024)} MB)"
        }

    non_object_cols = [col for col in COLUMNS if not ptypes.is_object_dtype(df[col])]
    if non_object_cols:
        return {
            "valid": False,
            "error": f"Columns {', '.join(non_object_cols)} are not strings"
        }

    for index, row in df.iterrows():
        for col in COLUMNS:
            pass
    
    return {
        "valid": True
    }
    