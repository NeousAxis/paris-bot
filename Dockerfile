# Étape 1 : installer Chrome et ChromeDriver
FROM python:3.13-slim AS base

# Installer dépendances système
RUN apt-get update && \
    apt-get install -y wget unzip gnupg2 ca-certificates && \
    # Ajouter la clé Google
    wget -qO- https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" \
      > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    # Installer ChromeDriver qui correspond à la version de Chrome
    CHROME_VER=$(google-chrome --version | awk '{print $3}') && \
    wget -q "https://chromedriver.storage.googleapis.com/${CHROME_VER}/chromedriver_linux64.zip" -O /tmp/chromedriver.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /var/lib/apt/lists/* /tmp/*

# Étape 2 : installer vos dépendances Python
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Étape 3 : copier le code et démarrer
COPY . .
EXPOSE 5000
CMD ["gunicorn", "server:app", "--bind", "0.0.0.0:5000"]