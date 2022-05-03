FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt update
RUN apt install -y libmagic-dev
RUN apt install dos2unix -y
RUN groupadd -r deepuser && useradd -r -g deepuser deepuser
WORKDIR /app
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/
EXPOSE 8009
RUN dos2unix /app/entry.sh
RUN chmod +x /app/entry.sh
ENTRYPOINT ["/app/entry.sh"]
