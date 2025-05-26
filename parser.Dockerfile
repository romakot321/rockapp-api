FROM infologistix/docker-selenium-python:alpine

WORKDIR /usr/src/app

RUN pip install bs4 aiohttp pydantic selenium selenium-stealth

COPY ./backend/mindat_parser/* /usr/src/app/

RUN mkdir /usr/src/app/cache -p

CMD python3 main.py
