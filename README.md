# 🎓 Quiz Generator Flow - CrewAI Multi-Agent System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![CrewAI](https://img.shields.io/badge/CrewAI-0.177.0%2B-green.svg)](https://crewai.com)
[![MLflow](https://img.shields.io/badge/MLflow-3.3.2%2B-orange.svg)](https://mlflow.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Benvenuto nel **Quiz Generator Flow**, un sistema avanzato di generazione automatizzata di quiz educativi basato su [CrewAI](https://crewai.com). Questo progetto implementa un **multi-agent AI system** che utilizza tecniche di **Retrieval-Augmented Generation (RAG)**, **vector databases** e **MLflow tracking** per creare quiz intelligenti e personalizzati per certificazioni tecniche.

## 🚀 Caratteristiche Principali

- 🤖 **CrewAI Flow Architecture**: Sistema multi-agente orchestrato con flow sequenziali
- 🔍 **RAG-Powered Generation**: Generazione domande basata su knowledge base vettoriale
- 📊 **MLflow Integration**: Tracking esperimenti e valutazione automatica con LLM Judge
- 🗄️ **Qdrant Vector Database**: Database vettoriale per ricerca semantica avanzata
- 📄 **Multi-format Output**: Quiz in Markdown e PDF, separati per versioni vuote e completate
- 🎯 **Certification-Specific**: Supporto per Azure AI-900, AI-102, Databricks e altre
- 🧪 **Quality Assurance**: Test automatizzati e valutazione qualità quiz
- 📈 **Performance Analytics**: Metriche dettagliate su rilevanza, fedeltà e correttezza

## 🏗️ Architettura del Sistema

Il sistema è organizzato in **5 Crews specializzati** che collaborano attraverso un **QuizGeneratorFlow**:

```
🔄 QuizGeneratorFlow
├── 📝 collect_user_input()          # Input utente e configurazione
├── 🗄️ initialize_vector_database()  # Setup knowledge base Qdrant
├── 📋 generate_quiz_template()      # Creazione template dinamici
├── 🔍 generate_quiz_with_rag_crew() # Generazione domande con RAG
├── 🛠️ create_final_quiz()          # Assemblaggio quiz finale
└── ✅ finalize_flow()              # Summary e cleanup
```

### 👥 Crews Specializzati

- **🔍 RagCrew**: Ricerca contestuale e generazione domande
- **📋 TemplateGeneratorCrew**: Creazione template quiz personalizzati  
- **🛠️ QuizMakerCrew**: Assemblaggio quiz finale con popolamento template
- **🎓 QuizTakerCrew**: Simulazione studente per completamento quiz
- **📊 QuizEvaluatorCrew**: Valutazione automatica qualità e metriche

## 📋 Prerequisiti

- **Python**: >=3.10, <3.14
- **UV Package Manager**: Per gestione dipendenze ottimizzata
- **Docker**: Per Qdrant vector database
- **Azure OpenAI**: Account e API key per LLM e embedding

## 🔧 Installazione

### 1. **Setup Ambiente**

```bash
# Clone del repository
git clone <repository-url>
cd FGBS_academy/quiz_generator

# Installazione UV (se non presente)
pip install uv

# Installazione dipendenze con CrewAI CLI
crewai install

# Alternativa con UV
uv sync
```

### 2. **Configurazione Environment**

Crea il file `.env` nella root del progetto:

```bash
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_API_VERSION=2025-01-01-preview
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
MODEL=gpt-4o
EMB_MODEL_NAME=text-embedding-ada-002

# Qdrant Vector Database
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=optional_api_key

# MLflow Tracking Server
MLFLOW_TRACKING_URI=http://127.0.0.1:5001
```

### 3. **Setup Infrastruttura**

```bash
# Avvia Qdrant Vector Database
docker run -p 6333:6333 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant

# Avvia MLflow Tracking Server (in terminale separato)
mlflow server --host 127.0.0.1 --port 5001
```

## 🚀 Modalità di Esecuzione

Il sistema supporta **due modalità principali** di esecuzione controllate dalla funzione `kickoff()` in `main.py`:

### 📝 **Modalità 1: Generazione Quiz Completa**

**Obiettivo**: Eseguire il flow completo di generazione quiz

**Configurazione** in `main.py`:
```python
def kickoff():
    """Alternative entry point for the flow (CrewAI convention)."""
    plot()
    main()          # ✅ Decommenta questa riga
    #evaluation_flow()  # ❌ Commenta questa riga
```

**Comando esecuzione**:
```bash
cd quiz_generator
crewai flow kickoff
```

**Flow eseguito**:
1. ✅ Raccolta input utente (provider, certificazione, topic)
2. ✅ Inizializzazione database vettoriale Qdrant
3. ✅ Generazione template quiz personalizzato
4. ✅ Ricerca RAG e generazione domande JSON
5. ✅ Assemblaggio quiz finale e conversione PDF
6. ✅ Summary e lista file generati

**Output**:
```
outputs/
├── AI_102_document_intelligence_template.md    # Template
├── AI_102_document_intelligence_questions.json # Domande JSON
├── AI_102_document_intelligence_quiz.md        # Quiz vuoto
└── AI_102_document_intelligence_quiz.pdf       # Quiz PDF vuoto
```

### 📊 **Modalità 2: Valutazione Quiz Esistenti**

**Obiettivo**: Valutare qualità quiz già generati con MLflow Judge

**Configurazione** in `main.py`:
```python
def kickoff():
    """Alternative entry point for the flow (CrewAI convention)."""
    plot()
    #main()         # ❌ Commenta questa riga  
    evaluation_flow()  # ✅ Decommenta questa riga
```

**Comando esecuzione**:
```bash
cd quiz_generator
crewai flow kickoff
```

**Processo**:
1. ✅ Carica quiz esistenti da `outputs/questions.json`
2. ✅ Esegue valutazione LLM Judge con MLflow
3. ✅ Genera metriche: answer_relevance, faithfulness, toxicity
4. ✅ Salva risultati in MLflow tracking server

**Accesso risultati**:
```bash
# Visualizza risultati MLflow
open http://127.0.0.1:5001
```

## 🎮 Guida all'Uso

### **Esperienza Utente Tipica**

```bash
# 1. Avvia il sistema
cd quiz_generator
crewai flow kickoff

# Output interattivo:
🚀 Starting Quiz Generator Flow...

📁 Available providers:
1. azure
2. databricks
Select provider (1-2): 1

🎓 Available certifications for azure:
1. AI_900
2. AI_102
Select certification (1-2): 2

🎯 Available topics for azure/AI_102:
1. document_intelligence
2. speech_service
3. foundry_foundry_local
Select topic (1-3): 1

❓ How many questions do you want? (3-10): 7
📝 Question type? (mixed/true_false/multiple_choice/open_ended): mixed

✅ User input selection collected successfully!
```

### **Struttura Dataset**

Organizza i tuoi documenti PDF nella cartella `dataset/`:

```
dataset/
├── azure/
│   ├── AI_900/
│   │   ├── fundamentals.pdf
│   │   ├── luis.pdf
│   │   └── service_azure.pdf
│   └── AI_102/
│       ├── document_intelligence.pdf
│       ├── speech_service.pdf
│       └── foundry_foundry_local.pdf
└── databricks/
    ├── certification_1/
    └── certification_2/
```

## 🔧 Personalizzazione

### **Configurazione Crews**

Modifica le configurazioni YAML per personalizzare comportamenti:

```bash
# Agenti specializzati
src/quiz_generator/crews/rag_crew/config/agents.yaml
src/quiz_generator/crews/quiz_maker_crew/config/agents.yaml

# Task e workflow
src/quiz_generator/crews/rag_crew/config/tasks.yaml
src/quiz_generator/crews/template_generator_crew/config/tasks.yaml
```

### **Tools Personalizzati**

Estendi le funzionalità creando nuovi tools:

```python
# Esempio: Custom RAG Tool
from crewai.tools import BaseTool

class CustomRagTool(BaseTool):
    name: str = "Custom RAG Search"
    description: str = "Ricerca personalizzata nel knowledge base"
    
    def _run(self, query: str) -> str:
        # La tua logica personalizzata
        pass
```

## 🧪 Testing

### **Test Suite Completa**

```bash
# Test tutti i componenti
pytest tests/ -v

# Test specifici
python tests/test_azure_ai900.py
python tests/test_complete_flow.py

# Test con coverage
pytest --cov=src tests/
```

## 📊 Monitoraggio e Analytics

### **MLflow Dashboard**

Accedi al dashboard MLflow per monitorare:

```bash
# Avvia MLflow UI
mlflow ui --host 127.0.0.1 --port 5001

# Accedi via browser
open http://127.0.0.1:5001
```

### **📊 Metriche Disponibili**
- **📝 answer_relevance**: Pertinenza risposta-domanda
- **✔️ ari grade level**: Leggibilità e comprensione delle domande
- **✔️ flesch kincaid grade level**: Livello scolastico delle domande
##### mancano le ground truth ancora per queste valutazioni sottostanti
- **✅ faithfulness**: Fedeltà al contesto fornito 
- **🎯 answer_similarity**: Similarità con ground truth
- **✔️ answer_correctness**: Correttezza risposta
- **🚫 toxicity**: Analisi contenuto tossico

### **Logs e Debugging**

```bash
# Abilita logging verboso
export CREWAI_LOG_LEVEL=DEBUG

# Visualizza flow grafico
python -c "from src.quiz_generator.main import plot; plot()"
```

## 📁 Struttura Output

### **File Generati per Quiz**

```
outputs/
├── {cert}_{topic}_template.md         # Template strutturato
├── {cert}_{topic}_questions.json      # Domande in formato JSON
├── {cert}_{topic}_quiz.md             # Quiz vuoto Markdown
├── {cert}_{topic}_quiz.pdf            # Quiz vuoto PDF
├── {cert}_{topic}_completed_quiz.md   # Quiz completato (se generato)
├── {cert}_{topic}_completed_quiz.pdf  # Quiz completato PDF
└── {cert}_{topic}_evaluation.md       # Report valutazione (se generato)
```

## 🐛 Troubleshooting

### **Problemi Comuni**

**🔧 Errore connessione Qdrant**:
```bash
# Verifica container Docker
docker ps | grep qdrant

# Riavvia se necessario
docker run -p 6333:6333 qdrant/qdrant
```

**🔑 Errore Azure OpenAI**:
```bash
# Verifica variabili ambiente
echo $AZURE_OPENAI_API_KEY
echo $AZURE_OPENAI_ENDPOINT

# Testa connessione
curl -H "api-key: $AZURE_OPENAI_API_KEY" "$AZURE_OPENAI_ENDPOINT/openai/models?api-version=2024-02-01"
```

**📄 Warning PDF parsing**:
I warning PDF sono automaticamente soppressi nel codice. Se persistono:

```python
# In utils/rag_qdrant_hybrid.py già implementato:
warnings.filterwarnings("ignore", message=".*Cannot set gray.*")
```

### **Logs Utili**

```bash
# Flow execution logs
python -m src.quiz_generator.main 2>&1 | tee execution.log

# CrewAI debug mode
CREWAI_LOG_LEVEL=DEBUG crewai flow kickoff
```

## 🤝 Contribuire

### **Workflow Contribuzioni**

1. **Fork** del repository
2. **Crea feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push branch**: `git push origin feature/amazing-feature`
5. **Crea Pull Request**

### **Standard Codice**

```bash
# Linting e formatting
black src/ tests/
flake8 src/ tests/
mypy src/

# Test prima di PR
pytest tests/ --cov=src
```

## 📚 Documentazione Avanzata

- 📚 **[FLOW_DOCUMENTATION.md](FLOW_DOCUMENTATION.md)**: Guida utente dettagliata
- 🌐 **[Sphinx Docs](quiz_generator/docs/_build/html/index.html)**: API reference
- 🎥 **[CrewAI Documentation](https://docs.crewai.com)**: Framework reference

## 📄 Licenza

Questo progetto è distribuito sotto licenza MIT. Vedi `LICENSE` per dettagli.

## 🙋‍♂️ Supporto

Per supporto, domande o feedback:

- 📖 **Documentazione**: [CrewAI Docs](https://docs.crewai.com)
- 🐛 **Issues**: [GitHub Repository](https://github.com/joaomdmoura/crewai)
- 💬 **Community**: [Discord CrewAI](https://discord.com/invite/X4JWnZnxPb)
- 🤖 **Chat**: [Docs Assistant](https://chatg.pt/DWjSBZn)

---
