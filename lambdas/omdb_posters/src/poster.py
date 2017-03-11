from __future__ import print_function
import ast
import boto3
import json
import requests

def poster(imdb_id):
    url = "http://img.omdbapi.com/?i={}&apikey={}&h={}".format(
            imdb_id,
            os.environ["OMDB_API_KEY"],
            os.environ["POSTER_HEIGHT"],
            )
    req = requests.get(url)

    if len(req.content) < 30:
        raise Exception(req.content)

    body = req.content
    key = '{}/poster.jpg'.format(imdb_id)
    s3 = boto3.resource('s3')
    s3.Bucket(settings.bucket).put_object(Key=key, Body=body, ACL="public-read")

def lambda_handler(event, context):
    for record in event["Records"]:
        for y in ast.literal_eval(record["Sns"]["Message"])["Records"]:
            key = y["s3"]["object"]["key"]
            imdb_id = key.split("/")[0]
            print("fetching poster for {}".format(imdb_id))
            poster(imdb_id)

    return True


if __name__ == "__main__":
    event = { "Records": [ {"Sns": { "Message": "tt2294629 tt0780622 tt0427312"} } ] }
    print(json.dumps(lambda_handler(event, None)))
