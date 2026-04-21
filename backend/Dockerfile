FROM python:3.9

WORKDIR /app

COPY . .

# system dependencies for mysqlclient
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# python dependencies
RUN pip install flask flask-mysqldb mysqlclient

EXPOSE 5000

CMD ["python", "app.py"]
