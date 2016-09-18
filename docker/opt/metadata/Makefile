#INPUT = s3://your_input_bucket/incoming/$(IMDB_ID).mp4
#BUCKET = your_output_bucket
IMDB_ID = $(shell basename $(INPUT) .mp4)
OUTPUT_DIR = s3://$(BUCKET)/processed/$(IMDB_ID)
.PHONY = clean width height duration in_s3 all upload delete_input

all: upload delete_input

metadata.txt: width height duration

clean:
	@rm -f video.mp4 metadata.txt frame.png

video.mp4:
	@echo "fetching video"
	@aws s3 cp $(INPUT) video.mp4

frame.png: video.mp4
	@echo "extracting frame"
	@rm -f frame.png
	@ffmpeg -i video.mp4 \
	  -ss 00:00:03       \
	  -vframes 1         \
	  frame.png          \
	  &> /dev/null

width: frame.png
ifeq ("$(wildcard metadata.txt)","metadata.txt")
	@sed -i '/^width:/d' metadata.txt
endif
	@echo "getting width"
	@printf 'width:' >> metadata.txt
	@identify -verbose "frame.png" \
	  | awk '/Geometry:/ { print $$2 }'   \
	  | tr 'x+' ' '                       \
	  | awk '{ print $$1 }'               \
	  >> metadata.txt

height: frame.png
ifeq ("$(wildcard metadata.txt)","metadata.txt")
	@sed -i '/^height:/d' metadata.txt
endif
	@echo "getting height"
	@printf 'height:' >> metadata.txt
	@identify -verbose "frame.png" \
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

upload: video.mp4 metadata.txt frame.png
	@echo "writing output to s3"
	@aws s3 cp video.mp4 $(OUTPUT_DIR)/video.mp4
	@aws s3 cp metadata.txt $(OUTPUT_DIR)/metadata.txt
	@aws s3 cp frame.png $(OUTPUT_DIR)/frame.png

delete_input:
	@echo "deleting input file from s3"
	@aws s3 rm $(INPUT)
