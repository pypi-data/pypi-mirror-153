FROM python:3.7-slim

WORKDIR .

COPY requirements.txt requirements.txt
COPY agent_service/main.py main.py
COPY agent_service/templates /templates

RUN pip install -r requirements.txt

CMD ["python", "-u", "main.py"]
