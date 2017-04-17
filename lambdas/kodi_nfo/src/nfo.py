from __future__ import print_function
import ast
import boto3
import json
import os
import re
from bs4 import BeautifulSoup

def write_to_s3(imdb_id, body):
    bucket = os.environ["MOVIES_BUCKET"]
    key = '{}/kodi.nfo'.format(imdb_id)
    s3 = boto3.resource('s3')
    s3.Bucket(bucket).put_object(Key=key, Body=body, ACL="public-read")

def read_s3_key(key):
    client = boto3.client('s3')
    object = client.get_object(Bucket=os.environ["MOVIES_BUCKET"], Key=key)
    return object["Body"].read()

def tag(key,values):
    xml = BeautifulSoup("", "html.parser")
    for value in values:
        value = str(value)
        d = BeautifulSoup("", "html.parser")
        d.append(d.new_tag(key))
        d.find(key).append(value.strip())
        xml.append(d)
    return xml

def ffprobe_value(regex, stream):
    for line in stream.split("\n"):
        if re.match(regex, line) is not None:
            return line.split("=")[1]

def nfo(imdb_id):
    nfo_key = "{}/kodi.nfo".format(imdb_id)
    omdb_key = "{}/omdb.json".format(imdb_id)
    ffprobe_key = "{}/ffprobe.txt".format(imdb_id)

    try:
        omdb_data = json.loads(read_s3_key(omdb_key))
    except:
        print("{} doesn't exist yet".format(omdb_key))
        return False

    try:
        ffprobe_data = read_s3_key(ffprobe_key)
    except:
        print("{} doesn't exist yet".format(ffprobe_key))
        return False

    ffprobe_streams = ffprobe_data.split("[STREAM]")

    xml = '''
        <movie>
          {title}
          {year}
          {runtime}
          {id}
          {thumb}
          {rating}
          {plot}
          {genre}
          {director}
          {actor}
          {mpaa}
          <fileinfo>
            <streamdetails>
              <video>
                {width}
                {height}
                {duration}
              </video>
            </streamdetails>
          </fileinfo>
        </movie>
    '''.format(**{
            "title": tag("title", [ omdb_data["Title"] ]),
            "year": tag("year", [ omdb_data["Year"] ]),
            "runtime": tag("runtime", [ omdb_data["Runtime"] ]),
            "id": tag("id", [ imdb_id ] ),
            "thumb": tag(
                        "thumb",
                        ["http://s3-{}.amazonaws.com/{}/{}/poster.jpg".format(
                            os.environ["MOVIES_BUCKET_REGION"],
                            os.environ["MOVIES_BUCKET"],
                            imdb_id,
                        )]),
            "rating": tag("rating", [ omdb_data["imdbRating"] ]),
            "plot": tag("plot", [ omdb_data["Plot"] ]),
            "genre": tag("genre", omdb_data["Genre"].split(",")),
            "director": tag("director", omdb_data["Director"].split(",")),
            "actor": tag("actor", omdb_data["Actors"].split(",")),
            "mpaa": tag("mpaa", [ omdb_data["Rated"] ] ),
            "width": tag("width", [ ffprobe_value(r"^width=", ffprobe_streams[1]) ]),
            "height": tag("height", [ ffprobe_value(r"^height=", ffprobe_streams[1]) ]),
            "duration": tag("duration", [ int( float(ffprobe_value(r"^duration=", ffprobe_streams[1])) / 60 ) ]),
        })

    return xml


def lambda_handler(event, context):
    print(event)
    for record in event["Records"]:
        for r in ast.literal_eval(record["Sns"]["Message"])["Records"]:
            imdb_id = os.path.dirname(r["s3"]["object"]["key"])
            print("generating kodi.nfo for {}".format(imdb_id))
            xml = nfo(imdb_id)
            write_to_s3(imdb_id, xml)
    return True

if __name__ == "__main__":
    with open('sample_event/tt0000000.json', 'r') as myfile:
        sample_event_json=myfile.read()
    event = json.loads(sample_event_json)
    print(lambda_handler(event, {}))
