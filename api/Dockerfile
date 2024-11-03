FROM python:3.11.10

# バッファリングを回避
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app/

COPY requirements.txt /usr/src/app/
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app/

CMD ["fastapi", "run", "app/genkou/app.py", "--port", "80", "--workers", "4"]



