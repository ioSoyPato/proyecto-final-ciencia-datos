# Base de Python
FROM python:3.10-slim

WORKDIR /code

RUN apt-get update && apt-get install -y procps && pip install -U pip && rm /etc/localtime && ln -s /usr/share/zoneinfo/America/Mexico_City /etc/localtime

# Instala las dependencias necesarias
RUN pip install streamlit requests

COPY ./app.py /code/

EXPOSE 8501

# Comando para ejecutar Streamlit
CMD ["streamlit", "run", "app.py"]
