# Inside the server, I'll use docker, instead of pipenv.

# This image is just for development:
# I'm not copying the source files, because I expect
# a bind mount somewere inside the container.

FROM tensorflow/tensorflow:2.1.0-gpu-py3

# Prepare user and home
RUN mkdir /home/ubuntu

RUN groupadd ubuntu && \
useradd -g ubuntu -d /home/ubuntu ubuntu && \
chown ubuntu:ubuntu /home/ubuntu
ENV HOME=/home/ubuntu

WORKDIR /home/ubuntu/

# Sw
RUN apt-get -y update && \
apt-get -y upgrade

# Project dependencies

# Basics
RUN apt-get -y install python3-pip bash-completion git 
# Opencv
RUN apt-get -y install libsm6 libxrender-dev

# Basics
RUN pip3 --no-cache-dir install -U wheel setuptools pip
# [packages] (tensorflow is already there)
RUN pip3 --no-cache-dir install -U numpy gym[atari]

# Go
USER ubuntu

ENV PATH="/home/ubuntu/bin:/home/ubuntu/.local/bin:$PATH"

ENTRYPOINT ["bash"]
