SETTINGS_BUCKET := $(shell aws cloudformation list-exports --query 'Exports[?Name==`s3strm-settings-bucket`].Value' --output text)
LAMBDA_MD5 = $(shell find . -iname \*.py -print0 | xargs -0 cat | md5)
LAMBDA_KEY = lambda/kodi_strm/${LAMBDA_MD5}.zip
LAMBDA_KEY_EXISTS := $(shell aws s3 ls "s3://${SETTINGS_BUCKET}/${LAMBDA_KEY}" &>/dev/null; echo $$?)

.PHONY: clean upload lambda_key

latest.zip: boto3
	@zip -9rq latest.zip $(shell find . -mindepth 1 ! -iname \*.zip ! -name Makefile ! -name setup.cfg)

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
endif

lambda_key:
	@echo ${LAMBDA_KEY}
