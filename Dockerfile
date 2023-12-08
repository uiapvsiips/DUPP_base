FROM python:3.8-alpine3.18
WORKDIR /app
COPY . /app
RUN pip install -r tg_requirements.txt
CMD ["python", "telegram/bot.py"]