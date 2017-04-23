import ast
import boto3
import json
import os
import sys

def has_custom_poster(imdb_id):
    client = boto3.client('s3')
    try:
        client.get_object(
                Bucket=os.environ["MOVIES_BUCKET"],
                Key="{}/poster-custom.jpg".format(imdb_id),
                )
    except:
        return False
    return True

def poster_key(imdb_id):
    if has_custom_poster(imdb_id):
        filename = "poster-custom.jpg"
    else:
        filename = "poster-omdb.jpg"
    return("{}/{}".format(imdb_id, filename))

def lambda_handler(event,context):
    client = boto3.client('s3')
    for record in event["Records"]:
        for r in ast.literal_eval(record["Sns"]["Message"])["Records"]:
            imdb_id = os.path.dirname(r["s3"]["object"]["key"])
            print("generating poster.jpg for {}".format(imdb_id))

            client.download_file(
                os.environ["MOVIES_BUCKET"],
                poster_key(imdb_id),
                "/tmp/poster.jpg",
            )

            try:
                client.upload_file(
                    "/tmp/poster.jpg",
                    os.environ["MOVIES_BUCKET"],
                    "{}/poster.jpg".format(imdb_id),
                    ExtraArgs={
                        'ContentType': 'image/jpeg',
                        'ACL': "public-read",
                    }
                )
            except:
                print("Failed to generate poster for {}".format(imdb_id))
                continue

    return True

if __name__ == "__main__":
    with open('sample_event/tt0000000.json', 'r') as myfile:
        sample_event_json=myfile.read()
    event = json.loads(sample_event_json)
    print(lambda_handler(event, None))
