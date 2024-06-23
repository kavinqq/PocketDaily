FROM python:3.11.6

WORKDIR /PocketDaily
COPY . /PocketDaily

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./entrypoint.sh /PocketDaily/entrypoint.sh
RUN chmod +x /PocketDaily/entrypoint.sh

ENTRYPOINT ["/PocketDaily/entrypoint.sh"]
