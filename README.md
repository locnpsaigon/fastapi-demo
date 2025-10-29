# fastapi-demo
A simple python fast api demo

1. Using docker:

docker run -d -p 8200:8000 --name fastapi-web \
-e POSTGRES_USER=postgres \
-e POSTGRES_PASSWORD=changeme \
-e POSTGRES_DB=sampledb \
-e POSTGRES_HOST=192.168.3.30 \
-e POSTGRES_PORT=5433 \
camel173/fastapi-demo:v1

2. Use compose file

services:
  postgres:
    image: postgres:15
    container_name: fastapi-db
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-postgres}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-changeme}
      POSTGRES_DB: ${POSTGRES_DB:-sampledb}
    ports:
      - "5433:5432"
    networks:
      - fastapi
    volumes:
      - pgdata:/var/lib/postgresql/data
  web:
    image: camel173/fastapi-demo:v1
    container_name: fastapi-demo
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ports:
      - "8100:8000"
    depends_on:
      - postgres
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-postgres}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-changeme}
      POSTGRES_DB: ${POSTGRES_DB:-sampledb}
      POSTGRES_HOST: ${POSTGRES_HOST:-postgres}
      POSTGRES_PORT: ${POSTGRES_PORT:-5432}
    networks:
      - fastapi
    volumes:
      - ./app:/app
networks:
  fastapi:
    driver: bridge
volumes:
  pgdata:

