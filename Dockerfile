# Usa una imagen de Python oficial
FROM python:3.11-slim

# Evita que Python genere archivos .pyc y permite ver logs en tiempo real
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Copia los archivos de requerimientos e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código
COPY . .

# Streamlit usa el puerto 8080 en Cloud Run por defecto
EXPOSE 8080

# Comando para ejecutar la app mapeando el puerto de Cloud Run
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
