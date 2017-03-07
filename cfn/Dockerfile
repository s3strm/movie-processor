FROM lambci/lambda:build
ENV AWS_DEFAULT_REGION ap-southeast-2
COPY ./src /usr/local/src
WORKDIR /usr/local/src

SHELL ["/usr/bin/python"]
CMD lambda.py
