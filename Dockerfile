FROM python:3.6-alpine
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
CMD [ "python", "app.py" ]
