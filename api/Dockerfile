FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

WORKDIR /app

COPY ./requirements.txt ./api/requirements.txt

RUN pip install --upgrade pip && pip install -r ./api/requirements.txt

COPY ./ ./api

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
