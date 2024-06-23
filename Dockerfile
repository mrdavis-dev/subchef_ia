# Usa una imagen base oficial de Python
FROM python:3.10-slim

# Instala gcc y otras dependencias necesarias
RUN apt-get update && apt-get install -y gcc

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo requirements.txt al directorio de trabajo
COPY requirements.txt .

# Crear y activar un entorno virtual, luego instalar las dependencias
RUN python3 -m venv /opt/venv \
    && . /opt/venv/bin/activate \
    && pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación al directorio de trabajo
COPY . .

# Exponer el puerto en el que se ejecutará la aplicación Streamlit
EXPOSE 8501

# Activar el entorno virtual y ejecutar la aplicación Streamlit
CMD ["/bin/bash", "-c", ". /opt/venv/bin/activate && streamlit run Homepage.py --server.port $PORT --server.address 0.0.0.0"]
