FROM python:3.7-slim-buster
WORKDIR /app

RUN pip3 --no-cache-dir install transformers
RUN pip3 --no-cache-dir install spacy
RUN pip3 --no-cache-dir install torchtext==0.6.0
RUN pip3 --no-cache-dir install fastapi
RUN pip3 --no-cache-dir install pydantic
RUN pip3 --no-cache-dir install uvicorn

COPY . .

RUN export PYTHONPATH=./

CMD ["python", "app.py"]