FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf &&  pip install -r requirements.txt

COPY . .

CMD ["python", "-u", "producer.py"]
