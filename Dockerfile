FROM python:2.7.10
WORKDIR /usr/src/app
COPY requirements.txt ./
COPY app.py ./
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python", "app.py"]
