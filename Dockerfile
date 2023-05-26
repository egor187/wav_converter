FROM python:3.11

WORKDIR /usr/src/app
COPY ./requirements.txt ./requirements.txt

RUN apt update && apt -y upgrade && apt install -y ffmpeg
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r ./requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]