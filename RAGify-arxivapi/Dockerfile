FROM python:3.12-slim

RUN pip install --upgrade pip 

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["app.py"]