FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

#ADD . . 

#EXPOSE 3000

COPY . .

#CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]
CMD ["gunicorn", "-b", "0.0.0.0:3000", "app:app"]

