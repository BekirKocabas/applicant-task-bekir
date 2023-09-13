FROM python:alpine
COPY . /app
WORKDIR /app
RUN pip install -U flask requests
EXPOSE 5000
CMD ["python", "player.py"]