VERSION = $(shell grep '^version = "' pyproject.toml | cut -d'"' -f2)

TARGETS := dist/tzconv-$(VERSION)-py3-none-any.whl
TARGETS += dist/tzconv-$(VERSION).tar.gz

.PHONY: build
build: $(TARGETS)

dist/tzconv-%-py3-none-any.whl:
	uv build --wheel .

dist/tzconv-%.tar.gz:
	uv build --sdist .

.PHONY: test
test:
	uv run pytest -v --cov=src

.PHONY: upload
upload: $(TARGETS)
	python3 -m twine upload $^

.PHONY: clean
clean:
	-rm -rf dist/
