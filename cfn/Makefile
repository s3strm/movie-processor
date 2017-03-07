STACK_NAME := $(shell ../bin/get_setting MOVIE_MP4META_STACK_NAME)
TEMPLATE = "file://./ffprobe.json"
LOG_GROUP_NAME = $(STACK_NAME)
CODE_BUCKET := $(shell ../bin/get_setting GENERAL_BUCKET)

.PHONY: clean log_group stack run build

run: build
	docker run ${TAG}

build:
	docker build . -t ${TAG}

deploy: log_group parameters.txt
	$(eval ACTION ?= $(shell ../bin/cloudformation_action $(STACK_NAME)))
	aws cloudformation $(ACTION)-stack            \
	  --stack-name "$(STACK_NAME)"                 \
	  --template-body "$(TEMPLATE)"                \
	  --parameters "$(shell cat ./parameters.txt)" \
	  --capabilities CAPABILITY_IAM                \
	  2>&1
	@aws cloudformation wait stack-$(ACTION)-complete \
	  --stack-name $(STACK_NAME)

log_group:
	-@aws logs create-log-group              \
		--log-group-name $(LOG_GROUP_NAME)

parameters.txt: clean
	$(eval PARAM_STR := 'ParameterKey=%s,ParameterValue=%s ')
	@printf $(PARAM_STR) "CodeBucket" $(CODE_BUCKET) >> parameters.txt

clean:
	@rm -f ./parameters.txt
