FROM python:3.10-slim

WORKDIR /source

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


EXPOSE 5555
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5555"]