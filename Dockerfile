# syntax=docker/dockerfile:1.2
# using ubuntu LTS version
FROM ubuntu:20.04 AS builder-image

# avoid stuck build due to user prompt
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install --no-install-recommends -y python3.9 python3.9-dev python3.9-venv python3-pip python3-wheel build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# create and activate virtual environment
# using final folder name to avoid path issues with packages
RUN python3.9 -m venv /home/ot_docker/venv
ENV PATH="/home/ot_docker/venv/bin:$PATH"

# install requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir fastapi[all] uvicorn[standard]
RUN pip3 install --no-cache-dir wheel
RUN pip3 install --no-cache-dir -r requirements.txt

FROM ubuntu:20.04 AS runner-image
RUN apt-get update \
    && apt-get install --no-install-recommends -y python3.9 python3-venv \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home ot_docker
COPY --from=builder-image /home/ot_docker/venv /home/ot_docker/venv

# Become docker user and create code dir
USER ot_docker
RUN mkdir /home/ot_docker/OTAnalytics-Backend

# Set current directory to Backend
WORKDIR /home/ot_docker/OTAnalytics-Backend

# Copy data from local dir 
# to docker build venv
COPY . .

# Open port 8000 
EXPOSE 8000

# make sure all messages always reach console
ENV PYTHONUNBUFFERED=1

# activate virtual environment
ENV VIRTUAL_ENV=/home/ot_docker/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


CMD ["uvicorn", "main:app" , "--reload", "--host", "0.0.0.0", "--port", "8000"]
