# original file https://github.com/aiogram/bot/blob/master/Makefile
include .env

tail := 200
PYTHONPATH := $(shell pwd):${PYTHONPATH}

PROJECT := wakeupbot
LOCALES_DOMAIN := bot
LOCALES_DIR := locales
VERSION := 0.1.0
PIPENV_VERBOSITY := -1

py := pipenv run
python := $(py) python

package_dir := app
code_dir := $(package_dir) tests

# =================================================================================================
# Base
# =================================================================================================

default:help

help:
	@echo $(PROJECT)

# =================================================================================================
# Initialize project
# =================================================================================================

install-env:
	pipenv update -d

install-hooks:
	$(py) pre-commit install

install-db: db
	sleep 3
	$(shell mkdir ./migrations/versions)
	$(MAKE) upgrade-db
	$(MAKE) db-stop

install-texts:
	$(shell mkdir ./locales)
	$(MAKE) pybabel-extract
	$(MAKE) texts-create-language language=en
	$(MAKE) texts-create-language language=ru

install: install-env install-hooks install-db install-texts
	@echo "$@ finished!"
# =================================================================================================
# Development
# =================================================================================================

requirements:
	pipenv lock -r > ./requirements.txt

seed-isort-config:
	$(py) seed-isort-config

isort:
	$(py) isort --recursive .

black:
	$(py) black .

flake8:
	$(py) flake8 .

lint: black flake8 seed-isort-config isort

entrypoint:
	pipenv run bash ../docker-entrypoint.sh ${args}

pybabel-extract:
	$(py) pybabel extract . \
    	-o ${LOCALES_DIR}/${LOCALES_DOMAIN}.pot \
    	--project=${PROJECT} \
    	--version=${VERSION} \
    	--copyright-holder=Illemius \
    	-k __:1,2 \
    	--sort-by-file -w 99

pybabel-update:
	$(py) pybabel update \
		-d ${LOCALES_DIR} \
		-D ${LOCALES_DOMAIN} \
		--update-header-comment \
		-i ${LOCALES_DIR}/${LOCALES_DOMAIN}.pot

texts: texts-update texts-compile
	@echo "$@ finished!"

texts-update: pybabel-extract pybabel-update

texts-compile:
	$(py) pybabel compile -d locales -D bot

texts-create-language:
	$(py) pybabel init -i locales/bot.pot -d locales -D bot -l ${language}

alembic:
	PYTHONPATH=$(shell pwd):${PYTHONPATH} $(py) alembic ${args}

upgrade-db:
	PYTHONPATH=$(shell pwd):${PYTHONPATH} $(py) alembic upgrade head

migration:
	PYTHONPATH=$(shell pwd):${PYTHONPATH} $(py) alembic revision --autogenerate -m "${message}"

downgrade-db:
	PYTHONPATH=$(shell pwd):${PYTHONPATH} $(py) alembic downgrade -1

_beforeStart: db upgrade-db texts-compile requirements

_app:
	$(py) python -m core

start:
	$(MAKE) _beforeStart
	$(MAKE) _app

git-pull:
	git pull origin

# =================================================================================================
# Docker
# =================================================================================================

docker-config:
	docker-compose config

docker-ps:
	docker-compose ps

docker-build:
	docker-compose build

db:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d db redis

db-stop:
	docker-compose stop db redis

docker-up:
	docker-compose up -d --remove-orphans

docker-stop:
	docker-compose stop

docker-down:
	docker-compose down

docker-destroy:
	docker-compose down -v --remove-orphans

docker-logs:
	docker-compose logs -f --tail=${tail} ${args}

# =================================================================================================
# Application in Docker
# =================================================================================================

app-create: _beforeStart db-stop docker-build docker-stop docker-up

app-recreate: app-down app-create

app-deploy: git-pull app-recreate

app-logs:
	$(MAKE) docker-logs args="bot"

app-stop: docker-stop

app-down: docker-down

app-start: docker-stop docker-up

app-destroy: docker-destroy
