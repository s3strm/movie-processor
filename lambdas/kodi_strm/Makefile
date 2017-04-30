export API_GATEWAY_DOMAIN = $(shell aws cloudformation list-exports --query 'Exports[?Name==`s3strm-api-gateway-domain`].Value' --output text)
export MOVIES_BUCKET = $(shell aws cloudformation list-exports --query 'Exports[?Name==`s3strm-movies-bucket`].Value' --output text)
export API_KEY = $(shell aws cloudformation list-exports --query 'Exports[?Name==`s3strm-api-key`].Value' --output text)

test:
	python ./src/strm.py

