# Open Tron Analytics Backend

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
        
        -
        
        -

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

ATR - 

Shifts