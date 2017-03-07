STACK_NAME = s3strm-ffprobe
STACK_TEMPLATE = "file://./ffprobe.yaml"

LAMBDA_BUCKET := $(shell ../bin/get_stack_output s3strm-settings SettingsBucket)
LAMBDA_KEY = lambda/ffprobe-${LAMBDA_MD5}.zip
LAMBDA_MD5 = $(shell find ./lambda -iname \*.py -print0 | xargs -0 cat | md5)

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
ifeq ( $(shell aws s3 ls s3://${LAMBDA_BUCKET}/${LAMBDA_KEY}),"" )
	@rm -f ./lambda/latest.zip  # make a new zip, but don't clean
	@make -C lambda latest.zip
	@aws s3 cp lambda/latest.zip s3://${LAMBDA_BUCKET}/${LAMBDA_KEY}
endif
