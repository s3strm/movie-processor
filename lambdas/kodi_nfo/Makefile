export MOVIES_BUCKET = $(shell aws cloudformation list-exports --query 'Exports[?Name==`s3strm-movies-bucket`].Value' --output text)
export MOVIES_BUCKET_REGION = $(shell echo ${AWS_DEFAULT_REGION})

test:
	python ./src/nfo.py

