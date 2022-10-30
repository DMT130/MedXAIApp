FROM python:3.9.15-bullseye

WORKDIR /app

COPY . .

RUN apt-get update

RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip3 install --upgrade pip

RUN pip3 install --no-cache-dir -r requirmentsv2.txt

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]