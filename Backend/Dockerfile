FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

# Create a startup script that handles database initialization gracefully
RUN echo '#!/bin/bash\n\
echo "Starting Flatera Backend..."\n\
echo "Attempting database initialization..."\n\
python init_postgres.py || echo "Database initialization failed or already exists"\n\
echo "Starting Gunicorn server..."\n\
exec gunicorn -b 0.0.0.0:5000 --timeout 120 --workers 2 app:app' > /app/start.sh

RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]
