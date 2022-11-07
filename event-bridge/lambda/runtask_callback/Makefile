PROJECT = $(CURDIR)
FUNCTION = $(PROJECT)
DIST_DIR ?= "$(BASE)"

all: build clean

.PHONY: clean build

clean:
	rm -rf build

build:
	$(info ************ Starting Build: $(PROJECT) ************)
	mkdir -p build
	python3 -m venv build/$(FUNCTION)
	. build/$(FUNCTION)/bin/activate; \
	pip3 install  -r requirements.txt -t ./ ;
