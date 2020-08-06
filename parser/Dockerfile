FROM python:3.8

WORKDIR /parser
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["bash", "run.sh"]