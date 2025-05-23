from python:3.12-slim

WORKDIR /app

RUN pip install bs4 aiohttp pydantic

COPY ./backend/mindat_parser/* /app

RUN mkdir /app/cache -p

CMD python3 main.py
