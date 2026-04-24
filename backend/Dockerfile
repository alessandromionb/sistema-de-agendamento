FROM python:3.11-slim
 
WORKDIR /app
 
# Copia e instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
 
# Copia o código da aplicação
COPY app/ ./app/
 
EXPOSE 8080
 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]