export KICKSTARTER_STACK_NAME = $(shell ./bin/get_setting MOVIE_MP4META_STACK_NAME)-kickstarter
export AWS_DEFAULT_REGION = $(shell ./bin/get_setting AWS_DEFAULT_REGION)

MOVIE_MP4META_STACK_NAME = $(shell ./bin/get_setting MOVIE_MP4META_STACK_NAME)
DOCKER_STACK_NAME = $(shell ./bin/get_setting DOCKER_STACK_NAME)

export KICKSTARTER_LAMBDA_BUCKET = $(shell ./bin/get_setting GENERAL_BUCKET)
export KICKSTARTER_LAMBDA_PREFIX = $(KICKSTARTER_STACK_NAME)
export KICKSTARTER_LAMBDA_ROLE_ARN = $(shell ./bin/get_stack_output $(MOVIE_MP4META_STACK_NAME) KickstarterRoleArn)

export ECS_CLUSTER = $(shell ./bin/get_stack_output $(DOCKER_STACK_NAME) Cluster)
export ECS_CONTAINER_NAME = $(shell ./bin/get_setting MOVIE_MP4META_ECR_REPO)
export ECS_TASK_DEFINITION = $(shell ./bin/get_stack_output $(MOVIE_MP4META_STACK_NAME) TaskDefinition)
export ECS_ENV_OVERRIDES = [{ "name": "SOMETHING", "value": "VALUE" }]
export ECS_OVERRIDES = { "containerOverrides": [{ "name": "$(ECS_CONTAINER_NAME)", "environment": $(ECS_ENV_OVERRIDES) }]}

deploy:
	-@make -C cfn stack
	@make -C docker push

kickstarter: deploy
	make -e -C ecs-kickstarter stack
