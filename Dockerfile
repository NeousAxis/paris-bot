### Étape 1 : build frontend si besoin (sinon sautez cette partie)
FROM node:18 AS assets
WORKDIR /app
COPY . .
# Si vous avez des assets à builder : RUN npm ci && npm run build

### Étape 2 : image finale Python + Chrome
FROM python:3.13-slim
# Installer Chrome & ChromeDriver
RUN apt-get update && \
    apt-get install -y wget unzip gnupg2 && \
    wget -qO- https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" \
      > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    CHROME_VERSION=$(google-chrome --version | awk '{print $3}') && \
    wget -q "https://chromedriver.storage.googleapis.com/${CHROME_VERSION}/chromedriver_linux64.zip" -O /tmp/chromedriver.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /var/lib/apt/lists/* /tmp/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste de l’app
COPY --from=assets /app/server.py ./server.py
# Si vous avez un dossier static issu du build frontend :
# COPY --from=assets /app/build ./static

# Expose et demarrage
EXPOSE 5000
CMD ["gunicorn", "server:app", "--bind", "0.0.0.0:5000"]