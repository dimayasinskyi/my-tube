FROM python:3.12.7
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
EXPOSE 7000
COPY . .
RUN chmod +x /usr/src/app/entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
