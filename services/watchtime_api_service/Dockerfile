FROM python

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY main.py /app/main.py

ENTRYPOINT [ "python3", "/app/main.py" ]