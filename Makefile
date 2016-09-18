deploy:
	make -C cfn stack
	make -C docker push
