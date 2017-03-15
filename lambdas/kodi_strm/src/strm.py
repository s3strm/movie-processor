from __future__ import print_function
import ast
import boto3
import json
import os

def strm(imdb_id):
    body = "{}/url?id={}".format(os.environ["API_GATEWAY_URL"], imdb_id)
    key = '{}/kodi.strm'.format(imdb_id)
    print("strm is: {}".format(body))
    s3 = boto3.resource('s3')
    s3.Bucket(os.environ["MOVIES_BUCKET"]).put_object(Key=key, Body=body, ACL="private")

def lambda_handler(event, context):
    for record in event["Records"]:
        for y in ast.literal_eval(record["Sns"]["Message"])["Records"]:
            key = y["s3"]["object"]["key"]
            imdb_id = key.split("/")[0]
            print("generating strm for {}".format(imdb_id))
            strm(imdb_id)

    return True

if __name__ == "__main__":
    with open('sample_event/tt0000000.json', 'r') as myfile:
        sample_event_json=myfile.read()
    event = json.loads(sample_event_json)
    lambda_handler(event, {})

####
