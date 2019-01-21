FROM debian:9.6-slim
RUN apt-get update && apt-get install -y \
    python \
    python-pip \
    libpng-dev \
    libblas-dev \
    liblapack-dev \
    gfortran \
    python-tk

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python ./app.py