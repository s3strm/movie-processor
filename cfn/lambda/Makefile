latest.zip: requirements
	zip -9rq latest.zip $(shell find . -mindepth 1 ! -iname \*.zip ! -name Makefile ! -name setup.cfg)

requirements:
	pip install boto -t ./

clean:
	rm -Rf ./boto*
	rm -f latest.zip

