#!/bin/bash

# Скрипт экспортирует зависимости проекта в файлы
# - /tmp/requirements.txt      Зависимости приложения
# - /tmp/requirements-dev.txt  Зависимости окружения разработки

export POETRY_VERSION=1.8.2
export POETRY_HOME=/opt/poetry

set -e -x

python3 -m venv $POETRY_HOME

source $POETRY_HOME/bin/activate

pip3 install -U pip wheel
pip3 install poetry==$POETRY_VERSION
poetry export --no-interaction --without-hashes --no-ansi --output=/tmp/requirements.txt
poetry export --with dev --no-interaction --without-hashes --no-ansi --output=/tmp/requirements-dev.txt
rm -r $POETRY_HOME
find /usr -name '*.pyc' -type f -delete

deactivate
