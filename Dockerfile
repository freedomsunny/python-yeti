FROM ubuntu:latest
ARG PROJECTNAME
ARG TZ=Asia/Shanghai
ENV PYTHONPATH=$PYTHONPATH:/opt/yeti/
# copy project
COPY $PROJECTNAME /opt/$PROJECTNAME
WORKDIR /opt/$PROJECTNAME/
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    apt update -y && \
    apt install -y python3 software-properties-common python3-distutils python3-apt wget vim && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    wget https://bootstrap.pypa.io/get-pip.py && \
    python3 get-pip.py && \
    pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

CMD ["/usr/bin/python3", "bin/yetid.py"]
