from __future__ import print_function
import ast
import boto3
import json
import os

def title(imdb_id):
    key = "{}/omdb.json".format(imdb_id)
    body = boto3.client('s3').get_object(Bucket=os.environ["MOVIES_BUCKET"], Key=key)["Body"].read()
    return json.loads(body)["Title"]

def strm(imdb_id):
    extinf = "#EXTINF:{}".format(title(imdb_id))
    url = "{}/url?id={}\n".format(os.environ["API_GATEWAY_URL"], imdb_id)
    body = "\n".join([extinf, url])
    key = '{}/kodi.strm'.format(imdb_id)
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
    s3 = boto3.client('s3')
    print("\nThe Document is:\n")
    print(
        s3.get_object(Bucket=os.environ["MOVIES_BUCKET"], Key="tt0000000/kodi.strm")["Body"].read()
    )
