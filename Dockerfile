FROM python:3.8-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
# Comment this if you are not in China.
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && pip config set install.trusted-host pypi.tuna.tsinghua.edu.cn
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py ./
COPY ./shadowmail ./shadowmail/

ENV FLASK_RUN_HOST=0.0.0.0

ENTRYPOINT [ "flask", "run" ]
