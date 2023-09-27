FROM python:3.10-bookworm
RUN python3 -m pip install aiogram docker
WORKDIR /app
COPY ./bot.py /app/bot.py
COPY ./docker_types.py /app/docker_types.py
CMD ["python3", "bot.py"]
