FROM python:3.9-buster

# install nginx
# RUN apt-get update && apt-get install nginx vim -y --no-install-recommends
# COPY nginx.default /etc/nginx/sites-available/default
# copy source and install dependencies
RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN apt-get update
# install for cv2
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get update \
    && apt-get install tesseract-ocr -y \
    python3 \
    #python-setuptools \
    python3-pip \
    && apt-get clean \
    && apt-get autoremove
RUN pip install -r requirements.txt

COPY ./app /app

WORKDIR /app

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
