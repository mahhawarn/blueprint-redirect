# ベースイメージの指定
FROM python:3.11

# 作業ディレクトリの設定
WORKDIR /app

# ホストの要件をコピーしてインストール
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# カレントディレクトリのファイルをコピー
COPY . /app
# Flaskアプリを実行
CMD gunicorn -w 4 -b 0.0.0.0:5000 app:app
