	
.PHONY: all
all: mypy rufflintfix ruffmt test

.PHONY: rufflintfix
rufflint:
	ruff check --fix

.PHONY: ruffmt
ruffmt:
	ruff format .

.PHONY: mypy
mypy:
	mypy main.py

.PHONY: test
test:
	pytest


