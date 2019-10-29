# Con esto creo la imagen de mi aplicación
#FROM python:2.7
FROM python:3.6

EXPOSE 80

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY app.py /app
CMD python app.py