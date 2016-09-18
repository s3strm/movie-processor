ECR_REPO = $(shell ../bin/get_setting ECR_REPO)
ECR_PATH := $(shell aws ecr get-login | awk -F/ '{ print $$NF }')/$(ECR_REPO):latest

push: tag
	$(shell aws ecr get-login)
	docker push $(ECR_PATH)

build:
	docker build -t $(ECR_REPO) .

tag: build
	docker tag $(ECR_REPO):latest $(ECR_PATH)

