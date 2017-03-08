STACK_NAME = s3strm-ffprobe
STACK_TEMPLATE = "file://./ffprobe.yaml"

LAMBDA_BUCKET := $(shell ../bin/get_stack_output s3strm-settings SettingsBucket)
LAMBDA_KEY = lambda/ffprobe-${LAMBDA_MD5}.zip
LAMBDA_MD5 = $(shell find ./lambda -iname \*.py -print0 | xargs -0 cat | md5)
LAMBDA_KEY_EXISTS ?= $(shell aws s3 ls "s3://${LAMBDA_BUCKET}/${LAMBDA_KEY}")
export AWS_SECRET_ACCESS_KEY
export AWS_DEFAULT_REGION
export AWS_ACCESS_KEY_ID

DOCKER_TAG = s3strm-ffprobe

.PHONY = upload_lambda

deploy: upload_lambda
	$(eval ACTION ?= $(shell ../bin/cloudformation_action $(STACK_NAME)))
	aws cloudformation ${ACTION}-stack            \
	  --stack-name "${STACK_NAME}"                 \
	  --template-body "${STACK_TEMPLATE}"                \
	  --parameters \
	    ParameterKey=CodeKey,ParameterValue=${LAMBDA_KEY} \
	  --capabilities CAPABILITY_IAM                \
	  2>&1
	@aws cloudformation wait stack-$(ACTION)-complete \
	  --stack-name $(STACK_NAME)

upload_lambda:
ifeq ($(LAMBDA_KEY_EXISTS),)
	@rm -f ./lambda/latest.zip  # make a new zip, but don't clean
	@make -C lambda latest.zip
	@aws s3 cp lambda/latest.zip s3://${LAMBDA_BUCKET}/${LAMBDA_KEY}
endif

docker_image:
	docker build . -t ${DOCKER_TAG}

test: docker_image
	docker run \
		-e AWS_SECRET_ACCESS_KEY \
		-e AWS_DEFAULT_REGION \
		-e AWS_ACCESS_KEY_ID \
		${DOCKER_TAG}
