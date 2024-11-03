FROM python:3.13.0

# To avoid buffering of stdout and stderr
# ENV PYTHONUNBUFFERED=1
ENV TZ=Asia/Tokyo

WORKDIR /usr/src/app/

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN python -m pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app/ /usr/src/app/

CMD ["fastapi", "run", "genkou/app.py", "--port", "80"]