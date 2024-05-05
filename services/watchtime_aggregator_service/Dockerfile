FROM python

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY ./*.py /app/

ENTRYPOINT [ "python3", "/app/main.py" ]