from __future__ import print_function
import os
import ast
import boto3
import json
import requests

def write_to_s3(imdb_id, body):
    bucket = os.environ["MOVIES_BUCKET"]
    key = '{}/omdb.json'.format(imdb_id)
    s3 = boto3.resource('s3')
    s3.Bucket(bucket).put_object(Key=key, Body=body, ACL="public-read")

def omdb(imdb_id):
    if imdb_id == "tt0000000":
        url = "http://www.omdbapi.com/?apikey={}&i={}&plot=full&r=json".format(os.environ["OMDB_API_KEY"], "tt0000001")
    else:
        url = "http://www.omdbapi.com/?apikey={}&i={}&plot=full&r=json".format(os.environ["OMDB_API_KEY"], imdb_id)

    req = requests.get(url)
    if len(req.content) < 30:
        raise Exception(req.content)
    return req.content

def lambda_handler(event, context):
    for record in event["Records"]:
        for y in ast.literal_eval(record["Sns"]["Message"])["Records"]:
            key = y["s3"]["object"]["key"]
            imdb_id = key.split("/")[0]
            print("fetching omdb json for {}".format(imdb_id))
            body = omdb(imdb_id)
            write_to_s3(imdb_id, body)

    return True

if __name__ == "__main__":
    with open('sample_event/tt0000000.json', 'r') as myfile:
        sample_event_json=myfile.read()
    event = json.loads(sample_event_json)
    lambda_handler(event, {})
