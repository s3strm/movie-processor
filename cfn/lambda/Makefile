latest.zip: requirements
	@zip -9rq latest.zip $(shell find . -mindepth 1 ! -iname \*.zip ! -name Makefile ! -name setup.cfg)

requirements:
	pip install boto==2.46.1 -t ./ --upgrade

clean:
	rm -Rf ./boto*
	rm -f latest.zip

