STACK_NAME = $(shell ../bin/get_setting STACK_NAME)
TEMPLATE = "file://./cfn.json"
LOG_GROUP_NAME = $(shell ../bin/get_setting LOG_GROUP_NAME)
ACTION := $(shell aws cloudformation describe-stacks --stack-name $(STACK_NAME) &>/dev/null && echo update || echo create)

PARAMETERS  = "ParameterKey=LogGroup,ParameterValue=$(LOG_GROUP_NAME)"

LOGGROUP_EXISTS := $(shell [[ -z $$(aws logs describe-log-groups --log-group-name-prefix ${LOG_GROUP_NAME} --query "logGroups[]" --output text) ]] && echo false || echo true )

log_group:
ifeq "$(LOGGROUP_EXISTS)" "false"
	aws logs create-log-group \
		--log-group-name $(LOG_GROUP_NAME) \
		--region ${AWS_DEFAULT_REGION}
endif

stack:
	@aws cloudformation $(ACTION)-stack            \
	  --stack-name "$(STACK_NAME)"                 \
	  --template-body "$(TEMPLATE)"                \
	  --parameters "$(PARAMETERS)"                 \
	  --capabilities CAPABILITY_IAM                \
	  2>&1
	@aws cloudformation wait stack-$(ACTION)-complete \
	  --stack-name $(STACK_NAME)
