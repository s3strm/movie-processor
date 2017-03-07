STACK_NAME = s3strm-ffprobe
TEMPLATE = "file://./ffprobe.yaml"

LAMBDA_BUCKET := $(shell ../bin/get_stack_output s3strm-settings SettingsBucket)
LAMBDA_KEY = lambda/ffprobe-${LAMBDA_MD5}.zip
LAMBDA_MD5 = $(shell find ./lambda -iname \*.py -print0 | xargs -0 cat | md5)

.PHONY: clean log_group stack run build

#run: build
#	docker run ${TAG}
#
#build:
#	docker build . -t ${TAG}

#deploy: parameters.txt
#	$(eval ACTION ?= $(shell ../bin/cloudformation_action $(STACK_NAME)))
#	aws cloudformation $(ACTION)-stack            \
#	  --stack-name "$(STACK_NAME)"                 \
#	  --template-body "$(TEMPLATE)"                \
#	  --parameters "$(shell cat ./parameters.txt)" \
#	  --capabilities CAPABILITY_IAM                \
#	  2>&1
#	@aws cloudformation wait stack-$(ACTION)-complete \
#	  --stack-name $(STACK_NAME)
#
#parameters.txt: clean
#	$(eval PARAM_STR := 'ParameterKey=%s,ParameterValue=%s ')
#	@printf $(PARAM_STR) "CodeBucket" $(CODE_BUCKET) >> parameters.txt
#
#clean:
#	@rm -f ./parameters.txt


upload_lambda:
ifeq ( $(shell aws s3 ls s3://${LAMBDA_BUCKET}/${LAMBDA_KEY}),"" )
	@rm -f ./lambda/latest.zip  # make a new zip, but don't clean
	@make -C lambda latest.zip
	@aws s3 cp lambda/latest.zip s3://${LAMBDA_BUCKET}/${LAMBDA_KEY}
endif
