FROM python:3.11-slim

# Ustawiamy katalog roboczy wewnątrz kontenera
WORKDIR /app

# Instalujemy zależności systemowe (potrzebne dla PostgreSQL)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Kopiujemy plik z wymaganiami i instalujemy biblioteki
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy resztę kodu aplikacji
COPY . .

# Domyślna komenda (uruchomimy ją przez docker-compose)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "divorce_project.wsgi:application"]