FROM lambci/lambda:build
ENV AWS_DEFAULT_REGION ap-southeast-2
COPY ./lambda /usr/local/src
WORKDIR /usr/local/src

ENV AWS_SECRET_ACCESS_KEY "secret"
ENV AWS_DEFAULT_REGION "us-east-1"
ENV AWS_ACCESS_KEY_ID "1234"

SHELL ["/usr/bin/python"]
CMD ffprobe.py
