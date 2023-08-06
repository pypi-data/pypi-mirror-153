FROM python:3.8
RUN apt update && apt install -y openssh-server
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
RUN pip3 install -e .
RUN mkdir ~/.ssh
ENTRYPOINT [ "pytest", "tests" ]