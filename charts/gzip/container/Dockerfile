FROM python:3.10-slim

RUN pip install --no-cache-dir \
        inaccel-gzip-zlib \
        gradio==3.20.* \
        pydantic==1.*

WORKDIR /gradio
COPY app.py .
COPY examples examples
ENTRYPOINT ["uvicorn", "--host=0.0.0.0", "--port=8080", "app:api"]
EXPOSE 8080
