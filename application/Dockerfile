FROM python:3.10

RUN apt-get update && apt-get install -y \
	python3-setuptools

RUN pip install --upgrade pip==21.2.4

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 4000

RUN chmod +x run.sh

CMD ["/app/run.sh"]