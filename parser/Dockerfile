FROM python:3.8

WORKDIR /parser
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN mkdir -p /content

COPY . .

CMD ["bash", "run.sh"]