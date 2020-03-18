FROM python:3.8-alpine

RUN apk --no-cache add graphviz
RUN pip install diagrams flask yapf

COPY src/server.py /

CMD python server.py
