FROM python:3.9-slim-buster


WORKDIR /src

COPY requirements.txt .
RUN python -m pip install -r requirements.txt 
COPY pyproject.toml setup.cfg setup.py ./
COPY ./api ./api/
RUN python -m pip install . --no-cache-dir --disable-pip-version-check


USER 2000:2000

EXPOSE 5000
CMD ["uvicorn", "api.main:app", "--port", "5000", "--host", "0.0.0.0"]

