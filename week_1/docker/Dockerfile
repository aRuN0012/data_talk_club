FROM python:3.9
run apt-get install wget
run pip install pandas psycopg2-binary SQLAlchemy pyarrow
workdir /app

copy ingestion.py ingestion.py

entrypoint ["python","ingestion.py"]