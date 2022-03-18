# Opentrons Analytics Backend

Link for [Github](https://github.com/mythreopen/OTA_Backend)

## How to use

1. Locally

   - Run production server

      ```python
      uvicorn main:app
      ```

   - Run development server

      ```python
      uvicorn main:app --reload
      ```

2. With Docker

   - Build current directory into docker image

      ```zsh
      docker build --tag ota_be .
      ```

   - Run container and publish to port 5000

      ```zsh
      docker run --publish 8000:5000 ot_be
      ```

3. With Docker Compose

    ```zsh
    docker-compose up
    ```

## Overview

`BaseURL = 'http://127.0.0.1'`

`BasePort = ':8000'`

`APIVersion: '/api/v2'`

`ServerURL: BaseURL + BasePort + APIVersion`

Currently the active routes we have are:

  1. Get Weekly Report Type

  2. Get Current Shifts

### Route Definitions

1. Get Weekly Report Type

   - Description:

      Returns JSON containing a Bool and an ATR Object containing the following columns:

        ```json
        "success": true,
        "data": {
          {
            "AccessionDate": ..., # Per Day
            "Hour": ...,          # Hour Per Day
            "Count": ...          # Total Per Hour Per Hour Day
          },
          {
            "AccessionDate": "02-04-2022", "Hour": 23, "Count": 5
          }
        }
        ```

   - Server: `URL = ServerURL + '/reports/get_weekly'`

   - HTTP Request: `POST`

   - Body:

      `content-type: application/json`

      ```python
      {
          "report_type": "AccessionTrackerReport"
      }
      ```

2. Get Shifts

   - Server: `URL = ServerURL + '/reports/get_shifts'`

   - HTTP Request: `GET`

### Reports and their data models

- ATR

| Name              | DType            | Description                                                                                                                                                                                                                                                                                                                                  |
|-------------------|------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| AccessionNumber   | String           | May contain numbers but also specific Lab areas (i.e. xyz-1234, abc-4567, etc.)                                                                                                                                                                                                                                                              |
| RequisitionNumber | String           | Contains both string and numbers                                                                                                                                                                                                                                                                                                             |
| CaseType          | String           |                                                                                                                                                                                                                                                                                                                                              |
| CollectionDate    | Date             |                                                                                                                                                                                                                                                                                                                                              |
| OrderingPhysician | String           |                                                                                                                                                                                                                                                                                                                                              |
| OrderingFacility  | String           |                                                                                                                                                                                                                                                                                                                                              |
| OrderingLocation  | String           |                                                                                                                                                                                                                                                                                                                                              |
| AccessionerName   | String           | Something to keep in mind for the names and the munging process is to make sure they are both following a standard that ensures a FName + LName format or an equivalent. If we compare by shift names, the shifts are formatted as Title + FName, LName and ensure that the name itself is in proper format AND fname + lname compatibility. |
| AccessionMonth    | Date -> Obj(str) | Even though the Date format is in %B-%Y, I prefer to keep it as a string due to using this to handle file data                                                                                                                                                                                                                               |
| MonthRange        | Date -> Obj(str) |                                                                                                                                                                                                                                                                                                                                              |
| WeekRange         | String           |                                                                                                                                                                                                                                                                                                                                              |
| AccessionDate     | Date             | The meat and sauce of the ATReports, we use this as a functional pivot point to handle the requests, responses, and data manipulation/visualization.                                                                                                                                                                                         |
| Hour              | Int64            |                                                                                                                                                                                                                                                                                                                                              |
| RackLocation      | String           |
| 'EMR #'           | String           | When adding to SQL Tables, the table may not able to read the special character which will cause confusion and problems|

- Shifts

| Name            | FirstShift | SecondShift | ThirdShift |
|-----------------|------------|-------------|------------|
| AccessionerName | String     | String      | String     |