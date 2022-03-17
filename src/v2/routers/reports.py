# # 
from calendar import week
from datetime import date, timedelta
import glob
import os
# # Fastapi
from fastapi import APIRouter, Request
import numpy as np
# # Utils
from src.v2.controllers import reports as reports_controller
# Data
import pandas as pd


# Router for FastAPI
router = APIRouter(
    prefix="/reports",
    tags=["reports"],
)


@router.post("/get_weekly")
async def get_weekly(req: Request):
    try:
        # Parse json to retrieve report type
        json = await req.json()
        report_type = json["report_type"]

        data = reports_controller.get_weekly(report_type)

        # Return JSON
        payload = {
            "success": True,
            "data": data
        }

    except Exception as error:
        payload = {
            "success": False,
            "data": [str(error)]
        }

    return payload


@router.get("/get_shifts")
async def get_shifts():  # req: Request):
    # try:
    # Today
    today = date.today()

    # A(bout a) week ago
    week_ago = today - timedelta(days=7)

    # Check if the resulting range spans 2 months
    # instead of 1. (i.e. feb27-mar5). Collect in
    # a list and grab uniques and then pass that
    # to another function to grab the respective
    # dataframes for that months shift dataframe.
    month_range = list(
        set(
            pd.date_range(
                week_ago, today).strftime("%B-%Y").tolist()
        )
    )

    acc_df = get_empl_shifts(month_range, "Accessioners")
    # print("ACC DF: ", acc_df)
    nonacc_df = get_empl_shifts(month_range, "NonAccessioners")
    # print(nonacc_df)

    response = {
        "success": True,
        "data": {
            "Accessioners": acc_df,
            "NonAccessioners": nonacc_df
        }
    }
    # except Exception as error:
    #     response = {
    #         "success": False,
    #         "data": [str(error)]
    #     }

    return response


def get_empl_shifts(date_range, report_type):
    shift_list = ["First", "Second", "Third"]

    # Target File for operations
    target_file = os.path.join(
        "data/Shift/", f"{date_range[0]}~*~{report_type}.parquet")

    # Glob the date from the specified target file
    date_glob = glob.glob(target_file)

    # Shift Period parquet file generator
    return shift_period_parquet(shift_list, date_glob)


def shift_period_parquet(list, file_list):
    dict_df = {}

    # Search for each Shift Period Parquet
    # in the globbed list
    for target_file in file_list:
        # print("FILE: ", target)
        # For each shift in the list
        # compare if it contains the given
        # shift value (1, 2, 3) and then
        # return that file as a df if true.
        for shift in list:
            if shift == "Third":
                target_df = pd.read_parquet(target_file).iloc[:, 1]
            else:
                target_df = pd.read_parquet(target_file).iloc[:, 0]
                
            # If shift in target file and not in dict
            # set default target shift
            if shift in target_file and shift not in dict_df:
                dict_df.setdefault(shift, target_df)

            if shift in target_file and shift in dict_df:
                dict_df[shift] = pd.concat(
                    [dict_df[shift], target_df], ignore_index=True)
    print(dict_df)
    return dict_df
