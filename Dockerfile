FROM python:3.10

WORKDIR /app

RUN apt-get update
RUN apt-get install -y xvfb

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN playwright install-deps
RUN playwright install chromium

RUN mkdir garmin_runs

COPY ./src .

CMD ["xvfb-run", "python", "sync.py"]