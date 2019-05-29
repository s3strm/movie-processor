from __future__ import print_function
import os
import ast
import boto3
import json
from subprocess import Popen
from subprocess import PIPE
from re import sub

def _ffprobe(imdb_id, url):
    print("Generating data for {}".format(imdb_id))
    ffprobe_path = os.getcwd() + "/bin/ffprobe"
    cmd = [ ffprobe_path, "-i", url, "-show_entries", "stream" ]
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    try:
        out[0]
    except IndexError:
        print("ffmpeg produced no output. The error was: {}".format(err))

    return out

def _upload(bucket, key, body):
    s3 = boto3.resource('s3')
    s3.Bucket(bucket).put_object(Key=key, Body=body, ACL="public-read")

def _url(bucket, key):
    s3 = boto3.client('s3')
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket,
            'Key': key
        }
    )
    return url

def lambda_handler(event, context):
    for record in event["Records"]:
        for y in json.loads(record["Sns"]["Message"])["Records"]:
            bucket = y["s3"]["bucket"]["name"]
            key = y["s3"]["object"]["key"]
            imdb_id = key.split("/")[0]
            url = _url(bucket,key)
            ffprobe_key = "{}/ffprobe.txt".format(imdb_id)
            ffprobe_body = _ffprobe(imdb_id, url)
            _upload(bucket, ffprobe_key, ffprobe_body)
    return True

if __name__ == '__main__':
    sample_event = { "Records": [ { "Sns": { "Message": "{ \"Records\": [ { \"eventVersion\": \"2.0\", \"eventTime\": \"1970-01-01T00:00:00.000Z\", \"requestParameters\": { \"sourceIPAddress\": \"127.0.0.1\" }, \"s3\": { \"configurationId\": \"testConfigRule\", \"object\": { \"eTag\": \"0123456789abcdef0123456789abcdef\", \"sequencer\": \"0A1B2C3D4E5F678901\", \"key\": \"tt4126340/video.mp4\", \"size\": 1024 }, \"bucket\": { \"arn\": \"arn:aws:s3:::s3strm-movies\", \"name\": \"s3strm-movies\", \"ownerIdentity\": { \"principalId\": \"EXAMPLE\" } }, \"s3SchemaVersion\": \"1.0\" }, \"responseElements\": { \"x-amz-id-2\": \"EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH\", \"x-amz-request-id\": \"EXAMPLE123456789\" }, \"awsRegion\": \"ap-southeast-2\", \"eventName\": \"ObjectCreated:Put\", \"userIdentity\": { \"principalId\": \"EXAMPLE\" }, \"eventSource\": \"aws:s3\" } , { \"eventVersion\": \"2.0\", \"eventTime\": \"1970-01-01T00:00:00.000Z\", \"requestParameters\": { \"sourceIPAddress\": \"127.0.0.1\" }, \"s3\": { \"configurationId\": \"testConfigRule\", \"object\": { \"eTag\": \"0123456789abcdef0123456789abcdef\", \"sequencer\": \"0A1B2C3D4E5F678901\", \"key\": \"tt4257858/video.mp4\", \"size\": 1024 }, \"bucket\": { \"arn\": \"arn:aws:s3:::s3strm-movies\", \"name\": \"s3strm-movies\", \"ownerIdentity\": { \"principalId\": \"EXAMPLE\" } }, \"s3SchemaVersion\": \"1.0\" }, \"responseElements\": { \"x-amz-id-2\": \"EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH\", \"x-amz-request-id\": \"EXAMPLE123456789\" }, \"awsRegion\": \"ap-southeast-2\", \"eventName\": \"ObjectCreated:Put\", \"userIdentity\": { \"principalId\": \"EXAMPLE\" }, \"eventSource\": \"aws:s3\" } ]}" } } ] }
    print(lambda_handler(sample_event, {}))
