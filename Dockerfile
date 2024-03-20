FROM python:3.10-buster

COPY . /root/watso

WORKDIR /root/watso

RUN pip install pipenv
RUN mkdir .venv
RUN pipenv install

CMD /root/watso/.venv/bin/uvicorn --factory app:create_app --host=0.0.0.0 --port=8000
