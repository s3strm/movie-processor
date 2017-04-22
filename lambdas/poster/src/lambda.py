import sys
import boto3
import os

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

    client.download_file(
        os.environ["MOVIES_BUCKET"],
        poster_key(event["imdb_id"]),
        "/tmp/poster.jpg",
    )

    try:
        client.upload_file(
            "/tmp/poster.jpg",
            os.environ["MOVIES_BUCKET"],
            "{}/poster.jpg".format(event["imdb_id"]),
            ExtraArgs={
                'ContentType': 'image/jpeg',
                'ACL': "public-read",
            }
        )
    except:
        return False

    return True

if __name__ == "__main__":
    event = { "imdb_id": "tt0000000" }
    print(lambda_handler(event, None))
