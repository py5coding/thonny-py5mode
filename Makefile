all: build_plugin

build_plugin:
	hatch build

clean:
	rm -rf dist
