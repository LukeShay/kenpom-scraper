init:
	source .venv/bin/activate
.PHONY: init

install:
	python3 -m pip install -Ur requirements.txt
.PHONY: install

setup:
	pyenv install 3.9.1
	python3 -m pip install --upgrade pip
	python3 -m pip install virtualenv
	python3 -m venv .venv
setup: init install
.PHONY: setup

format:
	python3 -m black ./
.PHONY: format

lint:
	python3 -m black --check ./
.PHONY: lint

scrape:
	python3 code_drivers/ken_pom_scraper.py roby@shaybrothers.com DqwtQ5eW1K
.PHONY: scrape

ratings:
	python3 code_drivers/ken_pom_ratings.py roby@shaybrothers.com DqwtQ5eW1K
.PHONY: ratings
