FROM andreilhicas/pipenv:alpine

COPY Pipfile Pipfile.lock /app/
COPY calculator /app/calculator

WORKDIR /app

RUN pipenv install

ENTRYPOINT ["pipenv", "run", "python", "-m", "calculator"]
