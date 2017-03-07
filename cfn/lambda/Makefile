latest.zip: requirements
	@zip -9rq latest.zip $(shell find . -mindepth 1 ! -iname \*.zip ! -name Makefile ! -name setup.cfg)

requirements:
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
		./six*
	rm -f latest.zip

