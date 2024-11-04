# Usar a imagem base do Python
FROM python:3.9-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar os arquivos necessários
COPY . .

# Instalar as dependências
RUN pip install -r requirements.txt

# Expor a porta do serviço
EXPOSE 5000

# Comando para rodar o aplicativo
CMD ["python", "-m", "src.api.main"]
