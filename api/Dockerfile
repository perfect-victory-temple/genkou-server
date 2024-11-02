FROM python:3.13.0

# To avoid buffering of stdout and stderr
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app/

# パスを修正（Dockerfileのディレクトリがルートになかったため）
COPY api/requirements.txt /usr/src/app/
RUN python -m pip install -r requirements.txt

COPY . /usr/src/app/

# 調べた感じ、デプロイ先でのコンテナ軌道のために以下のコマンドが必要
CMD ["uvicorn", "genkou.app:app", "--host", "0.0.0.0", "--port", "8000"]
