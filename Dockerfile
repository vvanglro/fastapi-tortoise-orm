FROM python:3.8

ADD requirements.txt .
RUN pip install --trusted-host pypi.python.org -r requirements.txt
WORKDIR /fastapi-main

CMD ["uvicorn", "run:app", "--reload","--host","0.0.0.0","--port","80"]