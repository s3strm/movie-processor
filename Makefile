STACK_NAME = s3strm-movie-processor
STACK_TEMPLATE = file://./cfn.yml
ACTION := $(shell ./bin/cloudformation_action $(STACK_NAME))

FFPROBE_KEY = $(shell make -C lambdas/ffprobe/src lambda_key)

DOCKER_TAG = s3strm-ffprobe
export AWS_SECRET_ACCESS_KEY
export AWS_DEFAULT_REGION
export AWS_ACCESS_KEY_ID

.PHONY = deploy upload docker_image test

deploy: upload
	aws cloudformation ${ACTION}-stack                             \
	  --stack-name "${STACK_NAME}"                                 \
	  --template-body "${STACK_TEMPLATE}"                          \
	  --parameters                                                 \
	    ParameterKey=FFprobeCodeKey,ParameterValue=${FFPROBE_KEY}  \
	  --capabilities CAPABILITY_IAM                                \
	  2>&1
	@aws cloudformation wait stack-${ACTION}-complete \
	  --stack-name ${STACK_NAME}

upload:
	@make -C lambdas/ffprobe/src upload

docker_image:
	docker build . -t ${DOCKER_TAG}

test: docker_image
	docker run \
		-e AWS_SECRET_ACCESS_KEY \
		-e AWS_DEFAULT_REGION \
		-e AWS_ACCESS_KEY_ID \
		${DOCKER_TAG}
