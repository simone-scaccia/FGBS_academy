# 📊 Quiz Generator Flow - Documentazione Completa

## 🏗️ ARCHITETTURA ATTUALE

```
📁 quiz_generator/
├── 📄 main.py                     # 🌊 Flow principale (CrewAI best practices)
├── 📁 utils/                      # 🛠️ Utilities modulari
│   ├── 📄 user_utils.py          # 👤 Gestione interazione utente
│   ├── 📄 database_utils.py      # 🗄️ Gestione database Qdrant
│   └── 📄 qdrant_utils.py        # ⚙️ Utilities Qdrant specifiche
├── 📁 tools/                     # 🔧 Strumenti RAG
│   ├── 📄 rag_qdrant_hybrid.py   # 🔍 Engine RAG con Qdrant
│   └── 📄 rag_qdrant_tool.py     # 🤖 Tool CrewAI per RAG
├── 📁 crews/                     # 👥 Agenti CrewAI
│   └── 📁 rag_crew/              # 🎯 Crew per generazione quiz
│       ├── 📄 rag_crew.py        # 👨‍💼 Agenti e task
│       └── 📁 config/            # ⚙️ Configurazioni YAML
└── 📁 dataset/                   # 📚 Database documenti PDF
    └── 📁 azure/                 # ☁️ Documenti Azure
        └── 📁 AI_900/            # 🎓 Certificazione AI-900
```

## 🔄 FLOW COMPLETO - Passo dopo Passo

### Step 1: 📝 Collect User Input
**File**: `utils/user_utils.py`
- **Funzione principale**: `get_user_selections(dataset_path)`
- **Processo**:
  1. Scansiona cartella `dataset/` per provider disponibili
  2. Mostra menu interattivo per selezione provider (es. 'azure')
  3. Scansiona subcartelle per certificazioni disponibili 
  4. Mostra menu per selezione certificazione (es. 'AI_900')
  5. Scansiona file PDF per topic disponibili
  6. Mostra menu per selezione topic specifico
- **Output**: `(provider, certification, topic)`

### Step 2: 🗄️ Initialize Vector Database
**File**: `utils/database_utils.py`
- **Funzione principale**: `initialize_database(provider, certification, dataset_base_path)`
- **Processo**:
  1. **Collection Naming**: Crea nome univoco collection: `{provider}_{certification}_chunks`
     - Esempio: `azure_ai_900_chunks`
  2. **Check Existing**: Verifica se collection esiste già
     - ✅ **Se esiste e contiene dati**: Salta inizializzazione (reusa)
     - ❌ **Se non esiste**: Procede con creazione
  3. **Document Loading**: 
     - Scansiona cartella `dataset/{provider}/{certification}/`
     - Carica tutti i file PDF con `load_pdf()` (con soppressione warning)
  4. **Text Splitting**: Divide documenti in chunks con overlap
  5. **Vector Creation**: 
     - Crea embeddings Azure OpenAI (text-embedding-ada-002)
     - Crea collection Qdrant con parametri ottimizzati
  6. **Upsert**: Inserisce chunks nel database vettoriale
- **Vantaggi Multi-Collection**:
  - 🎯 Una collection per certificazione
  - ⚡ Ricerche più veloci e precise
  - 💾 Riuso database esistenti
  - 🔄 No ri-elaborazione se già presente

### Step 3: 🤖 Generate Quiz with RAG Crew
**File**: `crews/rag_crew/rag_crew.py`
- **Agenti CrewAI**:
  - **👨‍🔬 Researcher**: Cerca informazioni con RAG Tool
  - **📊 Reporting Analyst**: Analizza e crea quiz strutturato
- **RAG Tool Configuration**:
  - **Provider-Aware**: `RagTool(provider="azure", certification="AI_900")`
  - **Collection-Specific Search**: Cerca solo nella collection corretta
- **Processo**:
  1. **Research Task**: Cerca informazioni relevant nel database
  2. **Quiz Generation**: Crea domande basate su contenuti trovati
  3. **Structured Output**: Formatta risultato finale

### Step 4: ✅ Finalize Flow
**File**: `utils/database_utils.py`
- **Funzione**: `save_quiz_results()`
- **Output**: File timestampato con risultati quiz

## 🛠️ MIGLIORAMENTI IMPLEMENTATI

### 1. 🔇 Soppressione Warning PDF
**Problema**: Warning rumorosi da PDF malformattati
```
Cannot set gray stroke color because /'P372' is an invalid float value
Cannot get FontBBox from font descriptor because None cannot be parsed as 4 floats
```
**Soluzione**: In `rag_qdrant_hybrid.py`
```python
def load_pdf(file_path: str) -> List[Document]:
    import warnings
    import logging
    
    # Suppress specific PDF parsing warnings
    warnings.filterwarnings("ignore", message=".*Cannot set gray.*")
    warnings.filterwarnings("ignore", message=".*Cannot get FontBBox.*")
    
    # Temporarily disable pdfminer logs
    pdfminer_logger = logging.getLogger('pdfminer')
    original_level = pdfminer_logger.level
    pdfminer_logger.setLevel(logging.ERROR)
```

### 2. 🗄️ Multi-Collection Support
**Problema**: Una sola collection per tutti i dati
**Soluzione**: Collection specifiche per certificazione
```python
def get_collection_name(provider: str, certification: str) -> str:
    clean_provider = "".join(c if c.isalnum() else "_" for c in provider.lower())
    clean_certification = "".join(c if c.isalnum() else "_" for c in certification.lower())
    return f"{clean_provider}_{clean_certification}_chunks"
```

**Vantaggi**:
- ✅ **Isolamento**: Ogni certificazione ha i suoi dati
- ✅ **Performance**: Ricerche più veloci su dataset ridotti  
- ✅ **Riuso**: No ri-elaborazione di dati esistenti
- ✅ **Scalabilità**: Facile aggiunta nuove certificazioni

### 3. 🎯 RAG Tool Collection-Aware
**Problema**: RAG Tool usava sempre collection default
**Soluzione**: RAG Tool configurabile
```python
class RagTool(BaseTool):
    def __init__(self, provider: Optional[str] = None, certification: Optional[str] = None):
        self.provider = provider
        self.certification = certification
    
    def _run(self, question: str, k: int):
        if self.provider and self.certification:
            return search_rag_with_collection(question, k, self.provider, self.certification)
```

## 🚀 ESECUZIONE

### Comando Principale
```bash
cd "quiz_generator"
python -m src.quiz_generator.main
```

### Flow di Esecuzione
1. **🚀 Starting Quiz Generator Flow...**
2. **📋 Provider Selection** → Mostra menu provider
3. **🎓 Certification Selection** → Mostra menu certificazioni  
4. **🎯 Topic Selection** → Mostra menu topic
5. **🗄️ Database Check** → Verifica/crea collection specifica
6. **🤖 RAG Crew Execution** → Genera quiz con agenti
7. **💾 Save Results** → Salva output timestampato

## 📁 FILE RIMOSSI (Cleanup)
- ❌ `main_flow.py` (versione obsoleta)
- ❌ `main_new.py` (versione obsoleta) 
- ❌ `tools/db_tools.py` (non utilizzato)
- ❌ `database_crew/` (cartella eliminata, logica spostata in utils)

## 🔧 CONFIGURAZIONE AMBIENTE

### Variabili Ambiente (.env)
```env
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment
QDRANT_URL=http://localhost:6333
```

### Dipendenze Principali
- CrewAI 0.165.1+ (con Flow support)
- Qdrant Client
- LangChain Community  
- Azure OpenAI
- PyMuPDF/PDFMiner

## 🎯 RISULTATO FINALE

Il Quiz Generator ora segue perfettamente le **CrewAI best practices**:
- ✅ **Main Flow nel main.py**
- ✅ **Utilities organizzate in cartelle dedicate**  
- ✅ **Gestione multi-database intelligente**
- ✅ **Output pulito senza warning PDF**
- ✅ **Architettura modulare e scalabile**
- ✅ **State management con Pydantic**
- ✅ **Reuso intelligente delle risorse**
