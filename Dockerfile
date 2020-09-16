FROM python:3.6-slim
RUN apt update -y && apt upgrade -y
RUN apt autoclean -y && apt autoremove -y
COPY . /SyncWrapperAPI
WORKDIR /SyncWrapperAPI
RUN pip3 install -r requirements.txt
EXPOSE 8080
ENTRYPOINT ["gunicorn", "SyncWrapperAPI:app", "--bind","0.0.0.0:8080", "--worker-class", "aiohttp.GunicornWebWorker"]