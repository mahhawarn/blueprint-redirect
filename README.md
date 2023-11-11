# blueprint-redirect

起動

flask -A app run


データベースマイグレーション

flask db init

flask db upgrade

flask db downgrade


Dockerfile

docker build -t blueprint-redirect .

docker run -p 5000:5000 -d blueprint-redirect

