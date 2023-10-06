FROM python:3.9-alpine
WORKDIR /app
COPY . /app/
RUN pip install Flask==2.3.3
ENTRYPOINT ["python", "-u", "server.py"]
EXPOSE 65432