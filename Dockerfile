
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# set working directory
WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/"
ENV PORT=8000

RUN pip install --upgrade pip

COPY ./requirements.txt /app/

RUN pip install -r requirements.txt

COPY . ./

WORKDIR /app/app

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]