SETTINGS_BUCKET := $(shell aws cloudformation list-exports --query 'Exports[?Name==`s3strm-settings-bucket`].Value' --output text)

ZIPABLE_FILES = $(shell find . -mindepth 1 ! -iname \*.zip ! -name Makefile ! -name setup.cfg ! -name .gitignore ! -path ./dateutil\* ! -path ./boto\* ! -path ./concurrent\* ! -path ./dateutil ! -path ./docutils\* ! -path ./futures\* ! -path ./jmespath\* ! -path ./python_dateutil\* ! -path ./s3transfer\* ! -path ./six\*)

LAMBDA_MD5 = $(shell cat ${ZIPABLE_FILES} | md5)
LAMBDA_KEY = lambda/kodi_strm/${LAMBDA_MD5}.zip
LAMBDA_KEY_EXISTS := $(shell aws s3 ls "s3://${SETTINGS_BUCKET}/${LAMBDA_KEY}" &>/dev/null; echo $$?)

.PHONY: clean upload lambda_key latest.zip

latest.zip: boto3
	@rm -f ./latest.zip
	@zip -9rq latest.zip ${ZIPABLE_FILES}

boto3:
	pip install boto3 -t ./ --upgrade

clean:
	rm -Rf \
		./boto* \
		./concurrent \
		./dateutil \
		./docutils* \
		./futures* \
		./jmespath* \
		./python_dateutil* \
		./s3transfer* \
		./six* \
	rm -f latest.zip

upload: latest.zip
ifneq ($(LAMBDA_KEY_EXISTS),0)
	@aws s3 cp latest.zip s3://${SETTINGS_BUCKET}/${LAMBDA_KEY}
else
	$(info s3://${SETTINGS_BUCKET}/${LAMBDA_KEY} already exists)
endif

lambda_key:
	@echo ${LAMBDA_KEY}
