FROM python:3.9.1
COPY ./serverParts /python-flask
WORKDIR /python-flask
RUN pip install -r requirements.txt
RUN python initialScript.py

CMD [ "python", "apis/http/api/endpoints.py" ]