FROM python:3.11

WORKDIR /app

COPY ./requirements.txt ./api/requirements.txt

RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf &&  pip install -r ./api/requirements.txt

COPY ./ ./api

RUN cd ./api

CMD alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000
