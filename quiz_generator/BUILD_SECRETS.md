# Gestione Multi-Segreti con Docker BuildKit - Pattern Avanzato

## Come costruire l'immagine con segreti multipli

Per costruire l'immagine Docker utilizzando segreti separati per ogni chiave Azure:

### PowerShell (Windows)
```powershell
$env:DOCKER_BUILDKIT=1
docker build `
  --secret id=azure-openai-api-key,src=.secrets/azure_openai_api_key.txt `
  --secret id=azure-openai-endpoint,src=.secrets/azure_openai_endpoint.txt `
  --secret id=azure-api-key,src=.secrets/azure_api_key.txt `
  --secret id=azure-api-base,src=.secrets/azure_api_base.txt `
  -t quiz-generator .
```

### Bash (Linux/Mac)
```bash
DOCKER_BUILDKIT=1 docker build \
  --secret id=azure-openai-api-key,src=.secrets/azure_openai_api_key.txt \
  --secret id=azure-openai-endpoint,src=.secrets/azure_openai_endpoint.txt \
  --secret id=azure-api-key,src=.secrets/azure_api_key.txt \
  --secret id=azure-api-base,src=.secrets/azure_api_base.txt \
  -t quiz-generator .
```

## Come funziona (Pattern Multi-Secret Avanzato)

1. **Sintassi BuildKit**: Il Dockerfile inizia con `# syntax=docker/dockerfile:1.7` per abilitare le funzionalità BuildKit
2. **Segreti separati**: Ogni chiave Azure è in un file separato nella cartella `.secrets/`
3. **Mount multipli**: Ogni segreto viene montato come variabile d'ambiente specifica (`env=AZURE_OPENAI_API_KEY`)
4. **Isolamento totale**: Ogni chiave è completamente isolata dalle altre
5. **Utilizzo diretto**: Le variabili sono disponibili direttamente nel comando RUN
6. **Ricostruzione runtime**: Il file `.env` viene ricostruito usando solo le variabili necessarie
7. **Distruzione automatica**: Tutti i segreti vengono automaticamente rimossi dopo il build step

## Vantaggi del Pattern CrewAI

- ✅ **Massima sicurezza**: Le chiavi non sono mai persistenti nei layer Docker
- ✅ **Utilizzo temporaneo**: I segreti esistono solo durante il comando RUN specifico  
- ✅ **No cache leaks**: I segreti non finiscono nella cache di build
- ✅ **No log exposure**: Le chiavi non appaiono nei log di build
- ✅ **Runtime support**: L'applicazione ha comunque accesso alle variabili d'ambiente

## Flusso di Sicurezza

```
.env file → Docker BuildKit → /run/secrets/env_vars → export → pip install → .env ricreato → container runtime
    ↑              ↑                    ↑                ↑           ↑              ↑
 Sorgente      Mounting           Lettura temp      Utilizzo    Installazione   App runtime
```

## Esecuzione del container

```powershell
docker run -it quiz-generator
```

Le variabili d'ambiente saranno disponibili per CrewAI tramite il file `.env` ricreato durante il build, ma i segreti originali sono stati distrutti dopo l'uso.