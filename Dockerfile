FROM python:3.14-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install -r requirements.txt 

COPY . .

RUN chmod +x start.sh

CMD ["./start.sh"]
