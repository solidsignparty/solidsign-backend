FROM python:3.12-slim

ADD poetry.lock pyproject.toml export_deps.sh /opt/app/

WORKDIR /opt/app/
RUN pip install gunicorn
RUN ./export_deps.sh && pip install -r /tmp/requirements.txt

ADD . /opt/app/
