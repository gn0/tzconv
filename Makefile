VERSION = $(shell cat setup.py | grep '^ *version="' | cut -d'"' -f2)

TARGETS := dist/tzconv-$(VERSION)-py3-none-any.whl
TARGETS += dist/tzconv-$(VERSION).tar.gz

.PHONY: build
build: $(TARGETS)

dist/tzconv-%-py3-none-any.whl:
	python3 -m build .

dist/tzconv-%.tar.gz:
	python3 -m build --wheel .

.PHONY: upload
upload: $(TARGETS)
	python3 -m twine upload $^
