FROM python:3.10.5

WORKDIR /src

COPY src/requirements.txt requirements.txt

RUN pip install -U -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
EXPOSE 5000 

CMD ["python", "src/app.py", "--host=0.0.0.0"]