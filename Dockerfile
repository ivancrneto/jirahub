FROM python:3.7.2-alpine3.8

RUN apk update \
    && apk add --no-cache make automake gcc g++ libffi-dev openssh-client libressl-dev python3-dev

RUN pip install --upgrade pip \
    && pip install pipenv

WORKDIR /code

ADD Pipfile /Pipfile
ADD Pipfile.lock /Pipfile.lock

RUN pipenv install --system --deploy --ignore-pipfile

ADD . /code

ENTRYPOINT ["python", "src/issues.py"]
