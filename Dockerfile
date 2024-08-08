FROM python:3.10.14-alpine3.20
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["fastapi", "run", "--port", "8080"]