FROM python:3.12.7
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
EXPOSE 7000
COPY . .
CMD ["gunicorn", "recommendation_service.wsgi:application", "--bind", "0.0.0.0:7000"]