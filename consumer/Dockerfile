FROM ubuntu:20.04
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/

RUN apt-get update -y \
    && apt-get install -y software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get install openjdk-8-jdk -y \
    && apt-get install python3.10 python3-pip -y \
    && export JAVA_HOME \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
    
ENV PYSPARK_PYTHON python3

WORKDIR /consumer

COPY . .

RUN pip3 install -r requirements.txt

CMD ["python3", "Script_spark.py"]
