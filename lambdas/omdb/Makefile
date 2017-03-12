export MOVIES_BUCKET = $(shell aws cloudformation list-exports --query 'Exports[?Name==`s3strm-movies-bucket`].Value' --output text)

test:
	python ./src/omdb.py

