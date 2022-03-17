
# # Fastapi
from fastapi import APIRouter, Request
# # Utils
from src.v2.controllers import data as data_controller
# from src.v2.controllers.data import database as db_controller
# Data
import pandas as pd

# Router for FastAPI
router = APIRouter(
    prefix="/data",
    tags=["data"],
)


@router.post("/uploadfile")
async def create_file(req: Request):
    """Get a list of bytes and convert that into
    a readable format. We then store the file by
    applying two techniques, cleaning / modeling
    and then storage / streaming

    Attributes
    ----------
    req: Request
        Incoming JSON from frontend client that
        is trying to upload a csv file containing data.

    Variables
    -------
    json: Byte[]
        incoming stream of bytes representing
        the csv data
    res: Dataframe<ReportType>
        Dataframe cons


    Return
    ------
    JSON
        return a munged and modeled json that contains the data
        in the form of a list that is 1 layer deep with a model
        that is dependent on its file name and file type.

    """
    try:
        # Parse multistream of bytes and capture data
        json = await req.json()
        # print(json)

        # Extract data from json and convert it
        # to a workable format.
        extraction = data_controller.extract_upload_data(json)
        # print("EXTRACTION DATA: ", extraction)

        # Convert the data to a dataframe structure
        df = pd.DataFrame(extraction["data"])

        # Clean the dataframe and convert the columns
        # to their proper and respective values
        data_controller.clean_upload(df, extraction["meta"])

        # Generate files based on report type
        data_controller.separate_df_to_parquet(df, extraction["meta"])

        # Return JSON
        payload = {
            "success": True,
            "data": extraction['meta']['type']
        }

    except Exception as error:
        payload = {
            "success": False,
            "data": [str(error)]
        }

    return payload
