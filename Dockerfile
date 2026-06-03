FROM python:3.11

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 7860

CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]