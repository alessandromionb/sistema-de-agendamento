FROM python:3.11-slim
 
WORKDIR /app
 
# Instala dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*
 
# Copia e instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
 
# Copia o código da aplicação
COPY app/ ./app/
 
EXPOSE 8080
 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]