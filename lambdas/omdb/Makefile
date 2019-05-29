export MOVIES_BUCKET = $(shell aws cloudformation list-exports --query 'Exports[?Name==`s3strm-movies-bucket`].Value' --output text)
export OMDB_API_KEY = $(shell aws cloudformation list-exports --query 'Exports[?Name==`s3strm-omdb-api-key`].Value' --output text)

test:
	python ./src/omdb.py

