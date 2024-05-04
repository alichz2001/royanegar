FROM python

WORKDIR /app

COPY requirements.txt requirements.txt

COPY main.py /app/main.py

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3", "/app/main.py" ]