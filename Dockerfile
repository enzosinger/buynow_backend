# Usar uma imagem base do Python 3.9 slim
FROM python:3.9-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar o arquivo requirements.txt para o container
COPY requirements.txt .

# Instalar as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação para o container
COPY . .

# Expor a porta 5000 para o Flask
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "app.py"]
