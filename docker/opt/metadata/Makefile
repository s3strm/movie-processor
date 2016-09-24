KEY = s3://your_input_bucket/tt123445/video.mp4
OUTPUT_DIR = s3:/$(shell dirname $$(echo $(KEY) | cut -d/ -f2-))
IMDB_ID = $(shell basename $(OUTPUT_DIR))

.PHONY = clean width height duration in_s3 all upload

all: clean upload

metadata.txt: width height duration

clean:
	-@aws s3 rm $(OUTPUT_DIR)/frame.jpeg
	-@aws s3 rm $(OUTPUT_DIR)/metadata.txt
	-@rm -f video.mp4 metadata.txt frame.jpeg

video.mp4:
	@echo "fetching video"
	@aws s3 cp $(KEY) video.mp4

frame.jpeg: video.mp4
	@echo "extracting frame"
	ffmpeg -ss 30 -i video.mp4 -qscale:v 2 -vframes 1 frame.jpeg

width: frame.jpeg
ifeq ("$(wildcard metadata.txt)","metadata.txt")
	@sed -i '/^width:/d' metadata.txt
endif
	@echo "getting width"
	@printf 'width:' >> metadata.txt
	@identify -verbose "frame.jpeg"        \
	  | awk '/Geometry:/ { print $$2 }'   \
	  | tr 'x+' ' '                       \
	  | awk '{ print $$1 }'               \
	  >> metadata.txt

height: frame.jpeg
ifeq ("$(wildcard metadata.txt)","metadata.txt")
	@sed -i '/^height:/d' metadata.txt
endif
	@echo "getting height"
	@printf 'height:' >> metadata.txt
	@identify -verbose "frame.jpeg" \
	  | awk '/Geometry:/ { print $$2 }'   \
	  | tr 'x+' ' '                       \
	  | awk '{ print $$2 }'               \
	  >> metadata.txt

duration:
ifeq ("$(wildcard metadata.txt)","metadata.txt")
	@sed -i '/^duration:/d' metadata.txt
endif
	@echo "getting duration"
	@printf 'duration:' >> metadata.txt
	@AtomicParsley video.mp4 -T 1              \
	  | awk '/^Movie duration/ { print $$3 }'  \
	  | cut -d. -f1                            \
	  >> metadata.txt

upload: video.mp4 metadata.txt frame.jpeg
	@echo "writing output to s3"
	@aws s3 cp metadata.txt $(OUTPUT_DIR)/metadata.txt
	@aws s3 cp frame.jpeg $(OUTPUT_DIR)/frame.jpeg
