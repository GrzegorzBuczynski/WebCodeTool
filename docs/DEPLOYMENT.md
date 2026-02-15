# 🚀 DEPLOYMENT - Wdrażanie do Produkcji

**Praktyczny przewodnik wdrażania systemu Multi-Agent do produkcji.**

---

## 📋 Pre-Deployment Checklist

- [ ] Kod przejdzie review
- [ ] Testy przechodzą (`python test_*.py`)
- [ ] .env skonfigurowany z API keys
- [ ] .gitignore zawiera .env
- [ ] Requirements.txt zaktualizowany
- [ ] Dokumentacja kompletna
- [ ] Backup bieżącego stanu
- [ ] Plan rollback'u

---

## 🏗️ Opcja 1: Linux Server (Rekomendowana)

### 1. Przygotowanie serwera

```bash
# Zaloguj się na serwer
ssh user@your-server.com

# Zainstaluj Python 3.8+
sudo apt-get update
sudo apt-get install python3.8 python3.8-venv python3-pip git

# Utwórz katalog aplikacji
mkdir -p /var/www/multi-agent
cd /var/www/multi-agent

# Sklonuj repo
git clone https://github.com/your-repo/multi-agent .
```

### 2. Setup aplikacji

```bash
# Utwórz virtual environment
python3.8 -m venv venv
source venv/bin/activate

# Zainstaluj zależności
pip install -r requirements.txt

# Konfiguracja .env
cp .env.example .env
nano .env  # Edytuj z rzeczywistymi wartościami
```

### 3. Systemd Service (automatyczny start)

```bash
# Utwórz service file
sudo nano /etc/systemd/system/multi-agent.service
```

Zawartość:
```ini
[Unit]
Description=Multi-Agent Task Decomposition System
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/multi-agent
Environment="PATH=/var/www/multi-agent/venv/bin"
Environment="PYTHONUNBUFFERED=1"
ExecStart=/var/www/multi-agent/venv/bin/python main.py

# Restart na crash
Restart=on-failure
RestartSec=10

# Logging
StandardOutput=append:/var/log/multi-agent/output.log
StandardError=append:/var/log/multi-agent/error.log

[Install]
WantedBy=multi-user.target
```

### 4. Uruchomienie

```bash
# Stwórz katalog logów
sudo mkdir -p /var/log/multi-agent
sudo chown www-data:www-data /var/log/multi-agent

# Włącz service
sudo systemctl enable multi-agent
sudo systemctl start multi-agent

# Sprawdzenie
sudo systemctl status multi-agent

# Logi
sudo tail -f /var/log/multi-agent/output.log
```

---

## 🐳 Opcja 2: Docker (Konteneryzacja)

### 1. Dockerfile

```dockerfile
FROM python:3.8-slim

WORKDIR /app

# Zainstaluj system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Skopiuj projektu
COPY . /app

# Zainstaluj Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Utwórz katalogi
RUN mkdir -p /app/results/{task_results,statistics,execution_logs}

# Expose port (jeśli będzie API)
EXPOSE 8000

# Environment
ENV PYTHONUNBUFFERED=1

# Run
CMD ["python", "main.py"]
```

### 2. docker-compose.yml

```yaml
version: '3.8'

services:
  multi-agent:
    build: .
    container_name: multi-agent
    environment:
      - AI_PROVIDER=openrouter
      - API_KEY=${API_KEY}
      - MODEL=meta-llama/llama-2-70b-chat
      - PERSISTENCE_DIR=/app/results
    volumes:
      - ./results:/app/results
      - ./.env:/app/.env:ro
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  # Opcjonalnie: Ollama dla offline
  # ollama:
  #   image: ollama/ollama:latest
  #   container_name: ollama
  #   ports:
  #     - "11434:11434"
  #   volumes:
  #     - ollama:/root/.ollama
  #   restart: unless-stopped

# volumes:
#   ollama:
```

### 3. Budowanie i uruchamianie

```bash
# Build image
docker build -t multi-agent:latest .

# Uruchom z docker-compose
docker-compose up -d

# Sprawdzenie
docker-compose logs -f multi-agent

# Stop
docker-compose down
```

---

## ☁️ Opcja 3: Cloud (AWS, GCP, Azure)

### AWS EC2 + Fargate

```bash
# 1. Utwórz ECR repository
aws ecr create-repository --repository-name multi-agent

# 2. Push image
docker build -t multi-agent:latest .
docker tag multi-agent:latest 123456789.dkr.ecr.us-east-1.amazonaws.com/multi-agent:latest
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/multi-agent:latest

# 3. Utwórz Fargate task definition
# (Przez AWS Console lub CloudFormation)

# 4. Deploy service
aws ecs create-service \
  --cluster my-cluster \
  --service-name multi-agent \
  --task-definition multi-agent:1 \
  --desired-count 1
```

### Google Cloud Run

```bash
# Buduj i deploy
gcloud run deploy multi-agent \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-env-vars "AI_PROVIDER=openrouter,API_KEY=sk-or-v1-..."
```

---

## 📊 Monitoring & Logging

### 1. Logs z systemd

```bash
# Real-time
sudo journalctl -u multi-agent -f

# Ostatnie 100 linii
sudo journalctl -u multi-agent -n 100

# Ostatnie 2 godziny
sudo journalctl -u multi-agent --since "2 hours ago"
```

### 2. Monitoring z Docker

```bash
# Stats
docker stats multi-agent

# Logs
docker logs -f multi-agent

# Wejdź do kontenera
docker exec -it multi-agent bash
```

### 3. Prometheus + Grafana (advanced)

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'multi-agent'
    static_configs:
      - targets: ['localhost:8000']
```

### 4. Log Aggregation (ELK Stack)

```python
# W agents.py - dodaj logging
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()
handler = logging.FileHandler('logs/app.json')
formatter = jsonlogger.JsonFormatter()
handler.setFormatter(formatter)
logger.addHandler(handler)
```

---

## 🛡️ Bezpieczeństwo

### 1. Zmienne Środowiskowe

❌ **Nigdy** w .env:
```
API_KEY=sk-KLUCZ
```

✅ **Zawsze** w secrets managera:
```bash
# AWS Secrets Manager
aws secretsmanager create-secret \
  --name multi-agent/api-key \
  --secret-string sk-or-v1-...
```

### 2. .gitignore (Sprawdzenie)

```bash
# Upewnij się:
cat .gitignore | grep ".env"
# Powinno być: .env

# Jeśli nie - dodaj:
echo ".env" >> .gitignore
git rm --cached .env
git commit -m "Remove .env from tracking"
```

### 3. Firewall

```bash
# Otwórz tylko potrzebne porty
sudo ufw allow 22/tcp      # SSH
sudo ufw allow 443/tcp     # HTTPS
sudo ufw allow 8000/tcp    # API (jeśli jest)
```

### 4. SSL/TLS (Jeśli API)

```bash
# Let's Encrypt
sudo certbot certonly --standalone -d your-domain.com

# W reverse proxy (nginx):
server {
    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    location / {
        proxy_pass http://localhost:8000;
    }
}
```

---

## 📈 Skalowanie

### Horizontalne (Multiple instances)

```bash
# Load balancer (nginx)
upstream multi-agent {
    server localhost:8001;
    server localhost:8002;
    server localhost:8003;
}

server {
    listen 80;
    location / {
        proxy_pass http://multi-agent;
    }
}
```

### Wertykalne (Bigger server)

```bash
# Zwiększ resources
# - CPU cores
# - RAM
# - Disk space
# - Network bandwidth
```

---

## 🔄 Backup & Recovery

### 1. Backup Strategy

```bash
# Daily backup skryptu
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups/multi-agent"
RESULTS_DIR="/var/www/multi-agent/results"

mkdir -p $BACKUP_DIR

# Backup results
tar -czf $BACKUP_DIR/results-$(date +%Y%m%d-%H%M%S).tar.gz $RESULTS_DIR

# Backup config
cp /var/www/multi-agent/.env $BACKUP_DIR/.env-$(date +%Y%m%d)

# Keep last 7 days
find $BACKUP_DIR -name "results-*.tar.gz" -mtime +7 -delete
```

### 2. Cron job

```bash
# Każdodziennie o 3 AM
0 3 * * * /home/user/backup.sh
```

### 3. Cloud Backup

```bash
# AWS S3
aws s3 sync /var/www/multi-agent/results s3://my-backup-bucket/multi-agent/results
```

---

## ⚠️ Disaster Recovery

### 1. Plan Rollback

```bash
# Jeśli deployment się nie powiódł
git checkout previous-version
docker-compose down
docker-compose up -d

# Lub przywróć backup
tar -xzf /backups/multi-agent/results-YYYYMMDD-HHMMSS.tar.gz
```

### 2. Health Check

```bash
#!/bin/bash
# health-check.sh

# Sprawdź czy aplikacja odpowiada
if ! curl -f http://localhost:8000/health; then
    echo "App unhealthy!"
    systemctl restart multi-agent
fi
```

---

## 📊 Cost Optimization

### 1. API Costs

```python
# W persistence.py - dodaj tracking kosztów
def track_cost(provider, model, tokens_used):
    costs = {
        'openrouter': 0.001,      # per 1K tokens
        'openai': 0.003,          # per 1K tokens
    }
    return (tokens_used / 1000) * costs.get(provider, 0)
```

### 2. Infrastructure Costs

| Provider | Instance | Monthly |
|----------|----------|---------|
| AWS EC2 | t3.medium | $30 |
| DigitalOcean | 2GB RAM | $12 |
| Heroku | Standard | $50 |

### 3. Optymalizacja

- Mniejszy max_recursion_depth → mniej API calls
- Caching → mniej requesty
- Batch processing → lepsze rates

---

## 📝 Post-Deployment

### 1. Monitoring

```bash
# Setup alerts na:
- Error rate > 5%
- Response time > 30s
- API quota exceeded
- Disk space < 10%
```

### 2. Updates

```bash
# Sprawdzanie nowych wersji
git fetch origin
git pull origin main
pip install -r requirements.txt
systemctl restart multi-agent
```

### 3. Performance Tuning

```bash
# Jeśli wolno:
1. Zwiększ num_executors (bardziej parallel)
2. Zmniejsz max_recursion_depth
3. Upgrade do większego server'a
4. Rozważ caching layer
```

---

## 🎯 Production Checklist

- [ ] Kod przetestowany
- [ ] .env z produkcyjnymi wartościami
- [ ] Backup strategy skonfigurowana
- [ ] Monitoring aktywny
- [ ] Logging zbierany
- [ ] SSL/TLS skonfigurowany
- [ ] Firewall ustawiony
- [ ] Health checks działające
- [ ] Recovery plan udokumentowany
- [ ] Dokumentacja aktualna

---

## 📞 Support & Troubleshooting

### Aplikacja nie startuje

```bash
# Sprawdzę logi
sudo journalctl -u multi-agent -n 50

# Sprawdzę Python
python3 -m py_compile agents.py

# Sprawdzę .env
grep -E "^[A-Z_]+=" .env
```

### High memory usage

```bash
# Zmniejsz num_executors
# Sprawdzę memory leaks
ps aux | grep python

# Restart'u
systemctl restart multi-agent
```

### API errors

```bash
# Sprawdzę klucz
echo "API_KEY: $API_KEY"

# Sprawdzę connectivity
curl https://api.openai.com

# Rotate klucz jeśli potrzeba
```

---

## 📚 Dodatkowe Zasoby

- [Docker Docs](https://docs.docker.com/)
- [Kubernetes Docs](https://kubernetes.io/docs/)
- [AWS Docs](https://docs.aws.amazon.com/)
- [Systemd Docs](https://www.freedesktop.org/software/systemd/man/)

---

**Wersja**: 1.0  
**Data**: 2024-12-07  
**Status**: Ready to Deploy ✅
