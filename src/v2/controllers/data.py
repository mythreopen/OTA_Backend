# # StdLib
import os
import re
from typing import Type
import pandas as pd
# #
from src.v2.utils import clean as clean_util
from src.v2.utils import convert as convert_util

# Extract the incoming csv data from the upload functionality.


def extract_upload_data(json):
    # Name of the incoming file
    file_name = json['file_name']

    file_type = csv_file_check(file_name)

    return {
        # CSV Data in multipart format
        "data": json['file']['data'],
        # File meta data
        "meta": {
            "type": file_type,
            "name": file_name,
        },
    }


def csv_file_check(file_name):
    if file_name == None:
        raise Exception("Invalid file name. Please send a proper file.")

    if "Shift" in file_name:
        return "Shift"
    else:
        # Strip the overarching report type with regex
        # and supply that as the folder to create.
        return re.sub(r'(\d+)[PM|AM]+\.csv', "", file_name, 0).strip()

# Clean the upload data
# check what the report type is
# and then apply the proper cleaning technique


def clean_upload(df, file_meta):
    # Extract file report type
    file_report_type = file_meta["type"]

    clean_dictionary = {
        "AccessionTrackerReport": clean_util.clean_atr_upload,
        "TATReport": None,
        "Shift": clean_util.clean_shifts_upload
    }

    return clean_dictionary[file_report_type](df)


# Separate the df by the main identifier
# of the df and save that to the parquet
def separate_df_to_parquet(df, file_meta):
    # Extract file report type
    file_report_type = file_meta["type"]

    separate_dictionary = {
        "AccessionTrackerReport": convert_util.atr_to_parquet,
        "TATReport": None,
        "Shift": convert_util.shift_to_parquet
    }

    return separate_dictionary[file_report_type](df, file_meta)
