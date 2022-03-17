# # Stdlib
from datetime import date
import os
import shutil

# Make sure file structure is correct


def local_dir_check():

    print("Checking directories....")

    # List of folders I want to generate
    data_dirs = [
        "AccessionTrackerReport",
        "TATReport",
        "ProblemTrackerReport"
        "Shift"
    ]

    [create_folder("data", data) for data in data_dirs]


def create_folder(dir_loc, fi_loc):

    if not os.path.exists('data'):
        print("Creating data directory...")
        os.makedirs('data')

    # File location for the folder
    # to be printed
    file_loc = f'{dir_loc}/{fi_loc}'

    if not os.path.exists(file_loc):
        print("Creating parquet directory in data...")
        os.makedirs(file_loc)


def remove_sensitive_data():
    if os.path.exists("data/") and os.path.isdir("data/"):
        shutil.rmtree("data/")
    with open("log.txt", mode="a+") as log:
        log.write("Deleted data folder at ", date.today())
    log.close()
