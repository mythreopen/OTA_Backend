# Stdlib
import os
import re
from time import strftime
# Pandas
import pandas as pd


# Separate incoming ATR data by date
# For each Accession Date group we
# create a file for it.
def atr_to_parquet(df, file_meta):
    # Extract file report type
    file_report_type = file_meta["type"]

    # Loop through the parquet file
    for date, df_group in df.groupby(["AccessionDate"]):
        file_name = date.date().strftime("%Y-%m-%d") + "~" + file_report_type
        to_parquet(df_group, "data", file_report_type, file_name)

# Look at the incoming file and split into parquet
# for each of their respective shifts


def shift_to_parquet(df, file_meta):
    # Extract file name
    file_name = file_meta["name"]

    # Split the incoming string and
    # return the current shift number
    shift_split = file_name.split(" - ")

    # Month_Year
    month_year = shift_split[0].split(" ")[0].replace("_", "-")

    # Shift Number
    # First, Second, and Third
    shift_num = shift_split[1].split(".")[0]

    # Remove file additionals
    # i.e. (0), (1), (2)
    shift_num = " ".join(shift_num.split(" ")[:2])
    # print("SPLIT SHIFT NUM: ", shift_num)

    # Shift File Name
    # Month and Year concatenated with the Current Shift Number
    shift_file_name = month_year + "~" + shift_num

    # Convert to Parquet
    # Accessioner
    to_parquet(
        # Extract only the accessioners
        get_accessioners(df),                   # DF
        "data",                                 # Top Dir
        file_meta["type"],                      # Report Type
        shift_file_name + "~Accessioners"       # Descriptor
    )

    # Non-Accessioner
    to_parquet(
        # Extract only the accessioners
        get_nonaccessioners(df),                # DF
        "data",                                 # Top Dir
        file_meta["type"],                      # Report Type
        shift_file_name + "~NonAccessioners"   # Descriptor
    )


# Generate incoming dataframe into a parquet file
def to_parquet(df, top_dir, report_type, descriptor):

    # Path for parquet files
    parquet_path = os.path.join(
        f"{top_dir}/{report_type}/", f"{descriptor}.parquet")

    # Check path presence and apply flow
    parquet_check(
        dataframe=df.astype(str),
        file_path=parquet_path,
        descriptor=descriptor
    )

# Check if the file exists based on the
# incoming path and its respective descriptors.


def parquet_check(dataframe, file_path, descriptor):
    # Check if the file exists
    if os.path.exists(file_path):
        print("=============================================")
        print(f"Parquet file for {descriptor} found at: ")
        print("\t" + file_path)
        print("Merging and concatenating file now...")
        print("=============================================")

        # Merges dataframe at file location and
        # at group location and then pandas
        # drops their duplicates.
        updated_dataframe = pd.concat(
            [dataframe, pd.read_parquet(file_path)]).drop_duplicates().reset_index(drop=True)

        # Overwrite original parquet file to path
        updated_dataframe.to_parquet(file_path)
    else:
        print("=============================================")
        print(f"Parquet file for {descriptor} not found: ")
        print("Generating file now...")
        print("=============================================")

        # Reset Index so the new parquet files are
        # now generated with proper indexing
        # remember to add 'drop=True'
        dataframe.reset_index(drop=True).to_parquet(file_path)

# # #
# Find accessioners by the given legend
# # #


def get_accessioners(df):
    accessioner_legend = ["a", "rec", "ov", "la",
                          "inc", "lvl", "o", "swab", "nm", "M"]

    return find_worker_type(df, accessioner_legend)


def get_nonaccessioners(df):
    nonaccessioner_legend = ["rp", "e", "hitpic", "pcr", "r"]

    return find_worker_type(df, nonaccessioner_legend)


def find_worker_type(df, shift_legend):
    return df[df.isin(shift_legend).any(axis=1)]
