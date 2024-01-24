FROM python:3.9

WORKDIR /app

COPY . .

RUN ls

RUN pip install -r requirements.txt

CMD ["python3", "-u", "./consumer.py"]