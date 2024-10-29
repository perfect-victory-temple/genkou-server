FROM python:3.13.0

# To avoid buffering of stdout and stderr
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app/

COPY requirements.txt /usr/src/app/
RUN python -m pip install -r requirements.txt
