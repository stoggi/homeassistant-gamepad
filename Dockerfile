FROM python:latest

RUN pip install homeassistant-api evdev

COPY buttons.py buttons.py

ENTRYPOINT ["python", "buttons.py"]