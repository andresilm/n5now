FROM python:3.12-slim

LABEL maintainer="andresluna2007@gmail.com"

WORKDIR /app

COPY . /app

EXPOSE 8000

RUN /bin/bash -c "source virtualenv/bin/activate && pip install --no-cache-dir -r requirements.txt"

CMD ["/bin/bash", "-c", "source virtualenv/bin/activate && python -m app.main"]
