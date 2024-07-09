# Utiliser une image de base de Python
FROM python:3.10.5-slim


# Définir le répertoire de travail
WORKDIR /app

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application code
COPY . .

 
ENV MONGO_URI=mongodb://mongoadmin:GRETA2024@4.233.138.30

ENV AZURE_KEY=2acf837fda7747f1ba80f86abf5943b0

ENV AZURE_ENDPOINT=https://rsy.cognitiveservices.azure.com/

# Exposer le port sur lequel l'application fonctionne
EXPOSE 8501

# Commande pour lancer l'application
CMD ["streamlit", "run", "main.py", "--server.port", "8501", "--server.address", "0.0.0.0"]