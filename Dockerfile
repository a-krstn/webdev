FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /webdev

RUN pip install --upgrade pip

COPY webdev/requirements.txt /webdev/
RUN pip install -r requirements.txt

COPY . .

COPY ./entrypoint.sh .

CMD ["./entrypoint.sh"]