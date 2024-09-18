# Usar uma imagem Python como base
FROM python:3.9-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar o requirements.txt para o container
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código para o diretório de trabalho do container
COPY . .

# Definir a variável de ambiente para garantir que a saída de log do Flask seja visível
ENV PYTHONUNBUFFERED=1

# Expor a porta que será usada pelo Flask
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["python", "app.py"]
