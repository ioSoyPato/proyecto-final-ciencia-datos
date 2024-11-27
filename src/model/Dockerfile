# Base oficial de Python
FROM python:3.10-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos necesarios a la imagen
COPY . .

RUN pip install --upgrade pip setuptools

# Instala las dependencias necesarias
RUN pip install fastapi uvicorn mlflow pydantic

# Expone el puerto en el que se ejecutará la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación con Uvicorn
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
