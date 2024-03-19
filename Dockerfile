FROM python:3.10-buster

COPY . /root/watso

WORKDIR /root/watso

RUN pip install pipenv
RUN mkdir .venv
RUN pipenv install

CMD /root/watso/.venv/bin/uvicorn app:create_app --uds /tmp/milvis.sock
