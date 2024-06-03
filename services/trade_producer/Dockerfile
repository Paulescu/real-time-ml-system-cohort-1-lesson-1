FROM python:3.10.3-slim-buster

# strea output to console
ENV PYTHONUNBUFFERED=1

# install poetry inside the container
RUN pip install poetry

WORKDIR /app

# copy all the source code into the container
COPY . /app

# install Python dependencies from the pyproject.toml file
RUN poetry install

CMD ["poetry", "run", "python", "src/main.py"]



