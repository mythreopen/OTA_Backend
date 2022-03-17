import pandas as pd
from scipy.fftpack import shift

###
# ATR CLEANING LOGIC
###


def clean_atr_upload(df):
    atr_string = [
        "AccessionNumber",
        "RequisitionNumber",
        "CaseType",
        "OrderingPhysician",
        "OrderingFacility",
        "OrderingLocation",
        "AccessionerName",
        "AccessionMonth",
        "MonthRange",
        "WeekRange",
        "RackLocation",
        "EMR #"
    ]
    atr_datetime = [
        "CollectionDate",
        "ReceivedDate",
        "AccessionDate",
    ]
    atr_int = [
        "Hour",
    ]
    # print("CLEAN ATR HIT: ", df)

    # # Convert all remaining nan to their respective fill type
    df[atr_string] = df[atr_string].fillna("").astype("string")

    # "Bug" happens when we convert to graph format.
    # Except it's built in https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_json.html
    #  ....For all other orients, the default is ‘epoch’.
    # The datetime conversion on all outgoing dataframes must
    # include date_format="iso"
    df[atr_datetime] = df[atr_datetime].fillna(
        "").apply(pd.to_datetime)
        
    # Fill 0's as the specified type integer.
    df[atr_int] = df[atr_int].fillna(0).astype(int)

# # #
# SHIFTS CLEANING LOGIC
# # #


def clean_shifts_upload(df):
    # Drop all exclusively NaN Columns
    df.dropna(axis=1, how='all')
    # acc_df = get_accessioners_detailed(df)
    # nonacc_df = get_nonaccessioners_detailed(df)
    # print("ACCESIONER DF:\n", acc_df)
    # print("NONACCESIONER DF:\n", nonacc_df)
    # df = df.astype(str)

# Detailed list of information
# contains MM/DD worked and at what position
# need to parse key table in order to fully
# flesh out models, not necessary though.
