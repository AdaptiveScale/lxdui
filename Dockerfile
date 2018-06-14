# docker run -it -p 15151:15151 -v /var/snap/lxd/common/lxd/unix.socket:/var/snap/lxd/common/lxd/unix.socket lxdui

FROM ubuntu

RUN apt update && apt install -y python3

ADD . /app
WORKDIR /app

RUN apt install -y python3-pip
RUN pip3 install setuptools
RUN python3 setup.py install

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
EXPOSE 15151

ENTRYPOINT ["python3", "run.py", "start"]