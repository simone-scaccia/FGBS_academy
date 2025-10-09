# Docker Healthcheck per Quiz Generator

## Configurazione Healthcheck

Il Dockerfile include un sistema completo di healthcheck che monitora:

### 🔍 **Componenti monitorati:**

1. **Processo CrewAI**: Verifica che il processo principale sia in esecuzione
2. **Azure OpenAI**: Controlla la connettività all'endpoint Azure
3. **MLflow** (opzionale): Verifica l'accessibilità del tracking server su `http://127.0.0.1:5001`
4. **Qdrant** (opzionale): Controlla la connessione al database vettoriale su `http://localhost:6333`

### ⚙️ **Parametri di configurazione:**

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3
```

- **`--interval=30s`**: Esegue il check ogni 30 secondi
- **`--timeout=10s`**: Timeout massimo per ogni check
- **`--start-period=60s`**: Periodo di grazia iniziale (60 secondi)
- **`--retries=3`**: Numero di retry prima di marcare come unhealthy

### 📋 **Script di healthcheck:**

Lo script `/usr/local/bin/healthcheck.sh` esegue questi controlli:

1. ✅ **Controllo processo**: `pgrep -f "crewai"`
2. ✅ **Connettività Azure**: `curl --connect-timeout 10 $AZURE_OPENAI_ENDPOINT`
3. ✅ **MLflow health**: `curl http://127.0.0.1:5001/health` (se disponibile)
4. ✅ **Qdrant health**: `curl http://localhost:6333/health` (se disponibile)

### 🚀 **Comandi utili:**

#### Verificare lo stato di salute:
```bash
docker ps
# La colonna STATUS mostrerà "healthy" o "unhealthy"
```

#### Controllare i log di healthcheck:
```bash
docker inspect --format='{{json .State.Health}}' <container_name> | jq
```

#### Eseguire manualmente l'healthcheck:
```bash
docker exec <container_name> /usr/local/bin/healthcheck.sh
```

### 🔧 **Personalizzazione:**

Per modificare i parametri di healthcheck, edita le righe nel Dockerfile:

```dockerfile
HEALTHCHECK --interval=<intervallo> --timeout=<timeout> --start-period=<periodo_iniziale> --retries=<retry> \
    CMD ["/usr/local/bin/healthcheck.sh"]
```

### 🐳 **Docker Compose:**

Se usi docker-compose, puoi sovrascrivere l'healthcheck:

```yaml
services:
  quiz-generator:
    image: quiz-generator
    healthcheck:
      test: ["/usr/local/bin/healthcheck.sh"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
```

### 📊 **Monitoraggio in produzione:**

L'healthcheck è particolarmente utile con orchestratori come:
- Docker Swarm
- Kubernetes (convertito in liveness/readiness probes)
- Container monitoring tools

Il container sarà automaticamente riavviato se i controlli falliscono per il numero specificato di retry.