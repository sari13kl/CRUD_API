# 1. Imagem base com Python
FROM python:3.12-slim

# 2. Define a pasta de trabalho dentro do container
WORKDIR /app

# 3. Copia e instala as dependências primeiro (melhor uso de cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copia o restante do projeto
COPY . .

# 5. Porta que a aplicação vai usar
EXPOSE 8000

# 6. Comando para iniciar o servidor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
