FROM python:3.10.5

COPY requirements.txt requirements.txt

RUN pip install -U -r requirements.txt

COPY . .

ENV FLASK_APP=testapp.py
EXPOSE 5000 

CMD ["python", "testapp.py", "--host=0.0.0.0"]