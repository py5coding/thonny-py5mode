all: build_plugin

build_plugin:
	rm -rf dist
	hatch build

clean:
	rm -rf dist
