AWS_DEFAULT_REGION := $(shell ../bin/get_setting AWS_DEFAULT_REGION)
GENERAL_BUCKET := $(shell ../bin/get_setting GENERAL_BUCKET)
MOVIE_BUCKET := $(shell ../bin/get_setting MOVIE_BUCKET)
MOVIE_POSTER := $(shell ../bin/get_setting MOVIE_POSTER)
MOVIE_POSTER_HEIGHT := $(shell ../bin/get_setting MOVIE_POSTER_HEIGHT)
MOVIE_POSTER_STACK_NAME := $(shell ../bin/get_setting MOVIE_POSTER_STACK_NAME)
OMDB_APIKEY := $(shell ../bin/get_setting OMDB_APIKEY)

CODE_MD5 := $(shell find ./lambda -iname \*.py -print0 | xargs -0 cat | md5)
CODE_ZIP := posters-$(CODE_MD5).zip
CODE_KEY := lambda/$(MOVIE_POSTER_STACK_NAME)/$(CODE_ZIP)

ACTION := $(shell ../bin/cloudformation_action $(MOVIE_POSTER_STACK_NAME))
TEMPLATE = "file://./posters.json"
PARAMETERS  = "ParameterKey=MovieBucketName,ParameterValue=$(MOVIE_BUCKET)"
PARAMETERS += "ParameterKey=CodeBucket,ParameterValue=$(GENERAL_BUCKET)"
PARAMETERS += "ParameterKey=CodeKey,ParameterValue=$(CODE_KEY)"

stack: upload_lambda
	aws cloudformation $(ACTION)-stack             \
	  --stack-name "$(MOVIE_POSTER_STACK_NAME)"    \
	  --template-body "$(TEMPLATE)"                \
	  --parameters ${PARAMETERS}                   \
	  --capabilities CAPABILITY_IAM                \
	  2>&1
	@aws cloudformation wait stack-$(ACTION)-complete \
	  --stack-name $(MOVIE_POSTER_STACK_NAME)

lambda_settings:
	@rm -f ./lambda/settings.py
	@echo 'api_key = "$(OMDB_APIKEY)"' >> ./lambda/settings.py
	@echo 'aws_default_region = "$(AWS_DEFAULT_REGION)"' >> ./lambda/settings.py
	@echo 'bucket = "$(MOVIE_BUCKET)"' >> ./lambda/settings.py
	@echo 'poster_height = "$(MOVIE_POSTER_HEIGHT)"' >> ./lambda/settings.py
	@echo 'poster_file = "$(MOVIE_POSTER)"' >> ./lambda/settings.py

zip: lambda_settings
	@rm -f ./posters-*.zip
	@cd ./lambda && \
	  zip -9rq ../$(CODE_ZIP) $(shell find .)

upload_lambda: zip
	@aws s3 cp $(CODE_ZIP) s3://$(GENERAL_BUCKET)/$(CODE_KEY)

