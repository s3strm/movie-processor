from __future__ import print_function
import os
import ast
import boto3
import json
from subprocess import call
from subprocess import Popen
from subprocess import PIPE
from re import sub
#import settings

def _ffprobe(imdb_id):
    ffprobe_path = os.getcwd() + "/bin/ffprobe"
    p = Popen([
        ffprobe_path,
        "-i", "https://s3-ap-southeast-2.amazonaws.com/s3strm-movies/tt0004972/video.mp4",
        "-show_entries",
        "stream"
        ], stdout=PIPE, stderr=PIPE)
    out = p.communicate()
    return _ffprobe_parser(out)

def _ffprobe_parser(text):
    out=[]
    for line in text.splitlines():
        if line == "[STREAM]":
            out.append({})
            continue
        try:
            key, value = line.split("=")
        except:
            continue

        out[-1].update({key: value})

    return out


def _metafile(imdb_id):
    return "/tmp/{}-metadata.txt".format(imdb_id)

def _metadata(imdb_id):
    width, height = _video_size(imdb_id)
    with open (_metafile(imdb_id), mode='w') as f:
        f.write('width:{}\n'.format(width))
        f.write('height:{}\n'.format(height))
        f.write('duration:{}\n'.format(_video_duration(imdb_id)))

def upload_metadata(imdb_id):
    _metadata(imdb_id)
    with open(_metafile(imdb_id), 'r') as f:
        print(f.read())

def lambda_handler(event, context):
    for record in event["Records"]:
        for y in ast.literal_eval(record["Sns"]["Message"])["Records"]:
            key = y["s3"]["object"]["key"]
            imdb_id = key.split("/")[0]
            #print("fetching metadata for {}".format(imdb_id))
            return print(_ffprobe(imdb_id))

if __name__ == "__main__":
    object1 = "{ 's3': { 'object': { 'key': 'tt2294629' } } }"
    object2 = "{ 's3': { 'object': { 'key': 'tt0780622' } } }"
    records = "{{ 'Records': [{}] }}".format(object1)
    event = { "Records": [ {"Sns": { "Message": records } } ] }
    print(json.dumps(lambda_handler(event, None)))
