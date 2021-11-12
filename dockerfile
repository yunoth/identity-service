FROM python:3.9.1
ADD . /python-flask
WORKDIR /python-flask
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python api.py