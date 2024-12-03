	
.PHONY: all
all: black mypy test

.PHONY: black
black:
	black .

.PHONY: mypy
mypy:
	mypy main.py

.PHONY: test
test:
	pytest


