FROM  python:alpine

COPY ./smartfox-greper.py .

RUN pip install requests paho-mqtt

ENTRYPOINT [ "python" ]

CMD [ "smartfox-greper.py" ]
