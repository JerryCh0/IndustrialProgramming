FROM python

ADD . /Main
WORKDIR /Main

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "main.py" ]
