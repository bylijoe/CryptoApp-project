FROM python:3.8.11-alpine3.14 as base

FROM base AS dependencias 

WORKDIR /install

RUN apk add --no-cache gcc musl-dev linux-headers
COPY src/requirements.txt .
RUN pip install --prefix=/install -r requirements.txt


FROM base

COPY --from=dependencias /install  /usr/local

WORKDIR /app
COPY src .

ENV FLASK_APP=run
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development
ENV MYSQL_HOST=mysql-server
ENV MYSQL_PORT=3306
ENV MYSQL_USER=kc_user
ENV MYSQL_PASSWORD=password
ENV MYSQL_DATABASE=movimientos

EXPOSE 5000

CMD ["flask", "run"]