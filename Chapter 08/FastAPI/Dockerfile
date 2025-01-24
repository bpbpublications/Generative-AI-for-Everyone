FROM python:3.11.7-slim

COPY ./requirements.txt  /app/requirements.txt

WORKDIR /app

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

COPY  app/* /app

ENTRYPOINT ["uvicorn"]

CMD ["--host", "0.0.0.0", "main:app"]