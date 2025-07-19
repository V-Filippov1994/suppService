FROM python:3.12

ENV PYTHONUNBUFFERED=1

RUN mkdir /backend_supp
WORKDIR /backend_supp

COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN chmod +x entrypoint.sh
