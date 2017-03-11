export API_GATEWAY_URL = $(shell aws cloudformation list-exports --query 'Exports[?Name==`s3strm-api-gateway-url`].Value' --output text)
export MOVIES_BUCKET = $(shell aws cloudformation list-exports --query 'Exports[?Name==`s3strm-movies-bucket`].Value' --output text)

test:
	python ./src/strm.py

