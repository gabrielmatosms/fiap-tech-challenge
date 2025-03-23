FROM python:3.12.7-slim

ENV PYTHONUNBUFFERED 1

RUN useradd -ms /bin/sh app

RUN mkdir /app
WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -U pip
RUN pip3 install --no-cache-dir -r requirements.txt

COPY ./docker/entrypoint.sh /entrypoint/entrypoint.sh
COPY . .

RUN chown app:app /app -R
USER app

EXPOSE 8009
CMD ["/entrypoint/entrypoint.sh"]
