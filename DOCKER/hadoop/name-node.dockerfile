FROM h_image

LABEL maintainer = "@Red_One"
WORKDIR /root

RUN apt-get update && apt-get -y install pip && \
    pip install jupyterlab 

RUN mkdir spark 
ENV PYSPARK_DRIVER_PYTHON='jupyter'
ENV PYSPARK_PYTHON=/usr/bin/python3
ENV PYSPARK_DRIVER_PYTHON_OPTS='lab --allow-root --ip=0.0.0.0 /root/spark'
# run pyspark in the background with 
# pyspark & 

