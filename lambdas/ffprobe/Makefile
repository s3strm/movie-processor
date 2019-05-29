export AWS_SECRET_ACCESS_KEY
export AWS_DEFAULT_REGION
export AWS_ACCESS_KEY_ID

DOCKER_TAG = s3strm-ffprobe

.PHONY = upload_lambda

test: docker_image
	docker run \
		-e AWS_SECRET_ACCESS_KEY \
		-e AWS_DEFAULT_REGION \
		-e AWS_ACCESS_KEY_ID \
		${DOCKER_TAG}

docker_image:
	docker build . -t ${DOCKER_TAG}

