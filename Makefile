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
	python3 code_drivers/scrapers/ken_pom/fan_match.py roby@shaybrothers.com DqwtQ5eW1K
.PHONY: fan-match

team-stats:
	python3 code_drivers/scrapers/ken_pom/team_stats.py roby@shaybrothers.com DqwtQ5eW1K
.PHONY: team-stats
