FROM python:alpine
COPY . /app
WORKDIR /app
RUN pip install -U flask requests
EXPOSE 5001
CMD ["python", "master.py"]