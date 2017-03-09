from __future__ import print_function
import os
import ast
import boto3
import json
from subprocess import Popen
from subprocess import PIPE
from re import sub

def _ffprobe(imdb_id, url):
    print("Generating data for {}".format(url))
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
            region = y["awsRegion"]
            imdb_id = key.split("/")[0]
            url = _url(bucket,key)
            ffprobe_key = "{}/ffprobe.txt".format(imdb_id)
            ffprobe_body = _ffprobe(imdb_id, url)
            _upload(bucket, ffprobe_key, ffprobe_body)
            return True

if __name__ == "__main__":
    object1 = "{ 's3': { 'object': { 'key': 'tt2294629' } } }"
    object2 = "{ 's3': { 'object': { 'key': 'tt0780622' } } }"
    records = "{{ 'Records': [{}] }}".format(object1)
    event = { "Records": [ {"Sns": { "Message": records } } ] }
    print(json.dumps(lambda_handler(event, None)))
