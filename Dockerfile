FROM python:3.12-alpine

COPY . /app
RUN pip install --break-system-packages --no-cache-dir ./app
WORKDIR /app/root

CMD ["latexdssite", "-i", "0.0.0.0", "-p", "80"]
EXPOSE 80
