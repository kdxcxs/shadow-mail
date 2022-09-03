FROM tiangolo/uwsgi-nginx-flask:python3.8

WORKDIR /app

COPY requirements.txt ./
# Comment this if you are not in China.
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && pip config set install.trusted-host pypi.tuna.tsinghua.edu.cn
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py ./main.py
COPY ./shadowmail ./shadowmail/
