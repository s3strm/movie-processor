MOVIES_BUCKET=$(
  aws cloudformation list-exports \
    --query 'Exports[?Name==`s3strm-movies-bucket`].Value' \
    --output text
)

function ffprobe() {
  imdb_id=$1
  aws s3 cp s3://${MOVIES_BUCKET}/${imdb_id}/ffprobe.txt -
}

function omdb() {
  imdb_id=$1
  aws s3 cp s3://${MOVIES_BUCKET}/${imdb_id}/omdb.json -
}

function kodi_strm() {
  imdb_id=$1
  aws s3 cp s3://${MOVIES_BUCKET}/${imdb_id}/kodi.strm -
}

function kodi_nfo() {
  imdb_id=$1
  aws s3 cp s3://${MOVIES_BUCKET}/${imdb_id}/kodi.nfo -
}

function poster() {
  imdb_id=$1
  aws s3 cp s3://${MOVIES_BUCKET}/${imdb_id}/poster.jpg -
}
