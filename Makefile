	
.PHONY: all
all: mypy rufflintfix ruffmt test

.PHONY: mypy
mypy:
	mypy .

.PHONY: rufflintfix
rufflint:
	ruff check --fix

.PHONY: ruffmt
ruffmt:
	ruff format .

.PHONY: test
test:
	pytest


