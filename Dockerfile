FROM python:3

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

RUN [ "alembic", "revision" , "--autogenerate", "-m", "mfu" ]
EXPOSE 4000

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4000" ]
