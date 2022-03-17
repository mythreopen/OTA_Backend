# Stdlib
import os
import pandas as pd


def get_weekly(report_type):
    # Get data folder location
    report_folder = os.path.join("data/", report_type)

    # Below sorts and filters the directory returning
    # a list of files in correct date order
    report_dir = sorted(
        filter(
            lambda x: os.path.isfile(os.path.join(report_folder, x)),
            os.listdir(report_folder)
        )
    )

    # Converts the last 7 of the directory
    # return a list of full paths to the
    # correct report files
    last_seven = [os.path.join(report_folder, date)
                  for date in report_dir[-7:]]

    # Lists last 7 days in YYYY-mm-dd format
    # for frontend use.
    past_week = [date.split("_")[0] for date in report_dir[-7:]]

    # Group by AccessionDate and Hour then sum occurences
    # This gives us the total per hour per day.
    # https://stackoverflow.com/questions/38933071/group-by-two-columns-and-count-the-occurrences-of-each-combination-in-pandas
    # Convert group of parquet files
    # to their respective dataframes
    if len(last_seven) == 1:
        # Bug occurs if 1 file is passed
        # as an array
        df_ls = pd.read_parquet(last_seven[0])
    else:
        df_ls = pd.read_parquet(last_seven)

    # Graph the weekly data resolution
    # and return it as it's own dataframe.
    # Maybe we can persist this in some form
    # of cache state?
    # Orient the json to the readable graph format
    json = get_weekly_report(df_ls, report_type).to_json(orient="records")

    return {
        'dailyISO': past_week,
        'weekData': json
    }


def get_weekly_report(df, report_type):

    weekly_dict = {
        "AccessionTrackerReport": get_weekly_atr,
        "TATReport": get_weekly_tat,
    }

    return weekly_dict[report_type](df)


def get_weekly_atr(df_list):
    graph_data_weekly = df_list.groupby(['AccessionDate', 'Hour']).size(
    ).to_frame(name="Count").reset_index()

    return graph_data_weekly


def get_weekly_tat(df_list):
    graph_data_weekly = df_list.groupby(['AccessionDate', 'Hour']).size(
    ).to_frame(name="Count").reset_index()

    return graph_data_weekly
