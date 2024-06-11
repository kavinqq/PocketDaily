FROM python:3.11.6

WORKDIR /PocketDaily

COPY . /PocketDaily

RUN pip install -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:8050", "--workers", "2", "index:app"]