FROM python:3.9-slim

WORKDIR /app

COPY ice_cream_main.py .

CMD ["python", "ice_cream_main.py"]