FROM ubuntu:16.04

RUN \
 apt-get update \
 && apt-get install -y software-properties-common python-software-properties apt-transport-https \
 && add-apt-repository ppa:deadsnakes/ppa \
 && apt-get update \
 && apt-get install -y build-essential python3.6 python3.6-dev curl

# Cleanup apt files so that image size is smaller.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ARG DEBIAN_FRONTEND=noninteractive


ENV PYTHONUNBUFFERED 1
RUN mkdir /test-scrap
WORKDIR /test-scrap
# Installing all requirements
ADD requirements.txt /test-scrap
RUN curl https://bootstrap.pypa.io/get-pip.py | python3.6
RUN python3.6 -m pip install -r requirements.txt
# Expose port
EXPOSE 8000
ADD . /test-scrap
