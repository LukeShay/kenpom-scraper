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

fan-match:
	python3 code_drivers/scrapers/ken_pom/fan_match.py
.PHONY: fan-match

fan-match-parser:
	python3 code_drivers/scrapers/ken_pom/fan_match_parser.py
.PHONY: fan-match-parser

team-stats:
	python3 code_drivers/scrapers/ken_pom/team_stats.py
.PHONY: team-stats
