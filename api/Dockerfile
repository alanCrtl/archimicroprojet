FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf &&  pip install --upgrade pip && pip install -r requirements.txt

COPY ./ /api

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 