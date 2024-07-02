FROM ubuntu:20.04

LABEL maintainer="andresluna2007@gmail.com"

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y python3 python3-pip curl make python3-venv

WORKDIR /app

COPY . /app

RUN make install

EXPOSE 8080

CMD ["uvicorn", "main:app" ,"--host", "127.0.0.1", "--port", "8080"]
