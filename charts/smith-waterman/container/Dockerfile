FROM python:3.10

RUN curl -sS https://setup.inaccel.com/repository | sh \
 && apt install --yes coral-api \
 && rm --force --recursive /var/lib/apt/lists/*

RUN git clone --depth 1 --recurse-submodules https://github.com/inaccel/klib /tmp/klib \
 && cd /tmp/klib \
 && gcc -D_KSW_MAIN ksw.c -lcoral-api -lz -o /bin/ksw \
 && rm --force --recursive /tmp/klib

FROM python:3.10-slim

RUN apt update \
 && DEBIAN_FRONTEND=noninteractive apt install --yes \
        curl \
 && rm --force --recursive /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
        gradio

RUN curl -sS https://setup.inaccel.com/repository | sh \
 && apt install --yes coral-api \
 && rm --force --recursive /var/lib/apt/lists/*

COPY --from=0 /bin/ksw /bin

WORKDIR /gradio
COPY app.py .
COPY examples examples
ENTRYPOINT ["uvicorn", "--host=0.0.0.0", "--port=8080", "app:api"]
EXPOSE 8080
