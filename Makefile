VERSION = $(shell grep '^version = "' pyproject.toml | cut -d'"' -f2)

TARGETS := dist/tzconv-$(VERSION)-py3-none-any.whl
TARGETS += dist/tzconv-$(VERSION).tar.gz

.PHONY: build
build: $(TARGETS)

dist/tzconv-%-py3-none-any.whl:
	uv build --wheel .

dist/tzconv-%.tar.gz:
	uv build --sdist .

.PHONY: upload
upload: $(TARGETS)
	python3 -m twine upload $^
