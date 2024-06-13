FROM python:3

WORKDIR /home/tim/docker-compose-data/raspy-station/src

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "main.py" ]
