FROM python:latest
RUN mkdir /superthon
WORKDIR /superthon
COPY requirements.txt /superthon
RUN pip3 install -r requirements.txt
COPY . /superthon
CMD ["python3","-m","superthon"]
