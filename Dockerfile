FROM python:3.9-alpine
WORKDIR /app
COPY server.py .
RUN pip install Flask==2.3.3
CMD ["python", "-u", "server.py"]
EXPOSE 3000