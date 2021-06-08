FROM python:3.8

RUN mkdir /workspace/
WORKDIR /workspace/
ADD . /workspace/
ENV EXTERNAL_PYPI_SERVER=https://mirrors.aliyun.com/pypi/simple/
RUN python -m venv /opt/venv \
    && /bin/bash -c "source /opt/venv/bin/activate" \
    && pip install --upgrade pip \
    && pip install -i $EXTERNAL_PYPI_SERVER --upgrade pip poetry \
    && poetry install
ENTRYPOINT ["poetry", "run"]
#CMD ["poetry","run","uvicorn", "run:app", "--reload","--host","0.0.0.0","--port","80"]