# 📊 Quiz Generator Flow - Documentazione Completa

## 🚀 Panoramica del Sistema

Il **Quiz Generator** è una piattaforma avanzata per la generazione automatizzata di quiz educativi che utilizza tecnologie all'avanguardia come **CrewAI Flow**, **Retrieval-Augmented Generation (RAG)**, **Qdrant Vector Database** e **MLflow** per creare un sistema completo di valutazione e apprendimento.

## 🎯 Funzionalità Principali

### ✨ **Generazione Quiz Intelligente**
- 🤖 **RAG-powered**: Utilizza documenti di certificazione per generare domande pertinenti
- 📊 **Multi-formato**: True/False, Multiple Choice, Open-ended questions
- 🎓 **Certificazioni Supportate**: Azure AI-900, AI-102 (futuro Databricks)
- 📝 **Template Dinamici**: Strutture quiz personalizzabili

### 🔄 **Pipeline Completa**
- 👤 **User Experience**: Interfaccia interattiva per selezione contenuti
- 🗄️ **Knowledge Base**: Database vettoriale con documenti di certificazione
- 📋 **Template Generator**: Creazione strutture quiz personalizzate
- 🎲 **Quiz Assembly**: Popolamento template con domande generate
- 🎓 **Student Simulation**: Simulazione risposte studente (working in progress)
- 📊 **Evaluation**: Valutazione automatica qualità quiz (working in progress)

### 📈 **Tracking & Analytics**
- 🔬 **MLflow Integration**: Tracking completo esperimenti
- 🧠 **LLM Judge**: Valutazione automatica con metriche avanzate
- 📊 **Performance Metrics**: Analisi qualità domande e risposte

## 🏗️ Architettura del Sistema

### 📁 **Struttura Progetto**
```
quiz_generator/
├── 🐍 src/quiz_generator/
│   ├── 🌊 main.py                     # QuizGeneratorFlow principale
│   ├── 👥 crews/                      # Agenti CrewAI specializzati
│   │   ├── 🔍 rag_crew/               # Ricerca e generazione domande
│   │   ├── 📋 template_generator_crew/ # Creazione template quiz
│   │   ├── 🛠️ quiz_maker_crew/        # Assemblaggio quiz finale
│   │   ├── 🎓 quiz_taker_crew/        # Simulazione studente
│   │   └── 📊 quiz_evaluator_crew/    # Valutazione automatica
│   ├── 🔧 tools/                      # Strumenti specializzati
│   │   ├── 🔍 rag_qdrant_tool.py      # Tool RAG per CrewAI
│   │   └── 📄 md_to_pdf_tool.py       # Conversione PDF
│   ├── 🛠️ utils/                      # Utilities sistema
│   │   ├── 👤 user_utils.py           # Interazione utente
│   │   ├── 🗄️ database_utils.py       # Gestione database
│   │   ├── ⚙️ qdrant_utils.py         # Utilities Qdrant
│   │   └── 🔍 rag_qdrant_hybrid.py    # Engine RAG
│   └── 📚 dataset/                    # Knowledge base
│       ├── ☁️ azure/                  # Documenti Azure
│       │   ├── 🎓 AI_900/             # Certificazione AI-900
│       │   └── 🎓 AI_102/             # Certificazione AI-102
│       └── 🧠 databricks/             # Documenti Databricks
├── 📤 outputs/                        # File generati
├── 🗄️ qdrant_storage/                 # Database vettoriale
├── 📚 docs/                           # Documentazione Sphinx
└── 🧪 tests/                          # Test suite
```

## 🔄 Flow di Esecuzione Completo

### **Step 1: 📝 Raccolta Input Utente** `@start()`

**Obiettivo**: Configurazione iniziale del sistema
**File**: `utils/user_utils.py`

**Processo**:
1. **🔍 Scansione Dataset**: Analizza struttura cartelle `dataset/`
2. **🏢 Selezione Provider**: Menu interattivo (azure, databricks, etc.)
3. **🎓 Selezione Certificazione**: Lista certificazioni disponibili
4. **🎯 Selezione Topic**: Lista argomenti da file PDF
5. **⚙️ Configurazione Quiz**: Numero domande e tipologia

**Output State**:
```python
state.provider = "azure"
state.certification = "AI_102" 
state.topic = "document_intelligence"
state.number_of_questions = 7
state.question_type = "mixed"
```

### **Step 2: 🗄️ Inizializzazione Database** `@listen(collect_user_input)`

**Obiettivo**: Setup knowledge base vettoriale
**File**: `utils/database_utils.py`

**Processo**:
1. **📋 Collection Naming**: `{provider}_{certification}_chunks`
2. **✅ Check Esistenza**: Verifica collection già presente
3. **📄 Caricamento PDF**: Estrazione testo da `dataset/{provider}/{certification}/`
4. **✂️ Chunking**: Divisione semantica documenti
5. **🧠 Embedding**: Azure OpenAI text-embedding-ada-002
6. **💾 Indicizzazione**: Upsert in Qdrant vector store

**Vantaggi**:
- 🎯 **Collection Isolate**: Una per certificazione
- ⚡ **Performance**: Ricerche mirate
- 🔄 **Riuso**: Skip re-processing se esistente

### **Step 3: 📋 Generazione Template** `@listen(initialize_vector_database)`

**Obiettivo**: Creazione struttura quiz personalizzata
**Crew**: **TemplateGeneratorCrew**

**Processo**:
1. **🎨 Design Template**: Struttura basata su configurazione utente
2. **🔖 Placeholders**: Segnaposto per popolamento automatico
   - `[TF_Question_X]` per True/False
   - `[MC_Question_X]` per Multiple Choice
   - `[Open_Question_X]` per domande aperte
3. **📝 Markdown Generation**: Template formattato professionalmente

**Output**: `outputs/{certification}_{topic}_template.md`

### **Step 4: 🔍 Generazione Domande RAG** `@listen(generate_quiz_template)`

**Obiettivo**: Creazione domande intelligenti con RAG
**Crew**: **RagCrew**

**Agenti**:
- **🕵️ Researcher**: Ricerca contestuale nel database
- **📊 Reporting Analyst**: Compilazione quiz strutturato

**Processo**:
1. **🔍 RAG Search**: Query mirate nel vector database
2. **🎯 Context Retrieval**: Estrazione passaggi rilevanti
3. **🤖 Question Generation**: LLM genera domande da contesto
4. **📝 JSON Structure**: Output strutturato per popolamento

**Configuration**:
```python
rag_crew = RagCrew(provider=provider, certification=certification)
inputs = {
    "topic": topic,
    "number_of_questions": 7,
    "question_type": "mixed"
}
```

**Output**: `outputs/{certification}_{topic}_questions.json`

### **Step 5: 🛠️ Assemblaggio Quiz Finale** `@listen(generate_quiz_with_rag_crew)`

**Obiettivo**: Popolamento template con domande
**Crew**: **QuizMakerCrew**

**Processo**:
1. **🔄 Template Loading**: Carica template generato
2. **📊 JSON Parsing**: Analizza domande strutturate
3. **🔧 Placeholder Replacement**: Sostituisce segnaposto con contenuto
4. **📄 Markdown Generation**: Quiz finale formattato
5. **🖨️ PDF Export**: Conversione in PDF per distribuzione

**CRITICO**: Quiz **VUOTO** - nessuna risposta pre-compilata per domande aperte

**Output**: 
- `outputs/{certification}_{topic}_quiz.md` (quiz vuoto)
- `outputs/{certification}_{topic}_quiz.pdf` (PDF vuoto)

## Simulation Student and Evaluation Crews are working in progress
#### **Step 6: 🎓 Simulazione Studente** `@listen(create_final_quiz)` [Opzionale]

**Obiettivo**: Completamento quiz da parte di studente simulato
**Crew**: **QuizTakerCrew**

**Processo**:
1. **🧠 LLM-Only Knowledge**: Nessun accesso a RAG o ground truth
2. **✍️ Quiz Completion**: Risposte basate su conoscenza LLM
3. **📝 Answer Formatting**: Formattazione risposte corretta
4. **📄 PDF Generation**: Quiz completato separato

**Output**:
- `outputs/{certification}_{topic}_completed_quiz.md`
- `outputs/{certification}_{topic}_completed_quiz.pdf`

### **Step 7: 📊 Valutazione Automatica** `@listen(take_quiz)` [Opzionale]

**Obiettivo**: Analisi qualità quiz e risposte
**Crew**: **QuizEvaluatorCrew**

**Processo**:
1. **🔍 Content Analysis**: Analisi domande e risposte
2. **📊 Quality Metrics**: Difficoltà, chiarezza, pertinenza
3. **📈 Performance Report**: Report dettagliato valutazione

**Output**: `outputs/{certification}_{topic}_evaluation.md`

### **Step 8: ✅ Finalizzazione** `@listen(create_final_quiz)`

**Obiettivo**: Summary e cleanup
**Processo**:
1. **📋 Status Report**: Stato finale di tutti gli step
2. **📁 File Summary**: Lista file generati
3. **🚨 Error Handling**: Report errori eventuali
4. **🧹 Cleanup**: Chiusura risorse

## 🔧 Configurazione Tecnologica

### **Environment Variables** (.env)
```bash
# 🤖 Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_API_VERSION=2025-01-01-preview
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
MODEL=gpt-4o
EMB_MODEL_NAME=text-embedding-ada-002

# 🗄️ Qdrant Vector Database
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=optional_api_key

# 📊 MLflow Tracking
MLFLOW_TRACKING_URI=http://127.0.0.1:5001
```

### **Dipendenze Principali** (pyproject.toml)
```toml
dependencies = [
    "crewai[tools]>=0.177.0,<1.0.0",
    "langchain>=0.3.27",
    "langchain-openai>=0.2.14", 
    "qdrant-client>=1.15.1",
    "mlflow>=3.3.2",
    "pymupdf>=1.26.4",
    "markdown-pdf>=1.9",
    "pytest>=8.4.2"
]
```

## 🚀 Guida all'Uso

### **🔧 Installazione**
```bash
# Clone repository
git clone <repository_url>
cd quiz_generator

# Install dependencies
pip install -e .

# Setup environment
cp .env.example .env
# Edit .env with your credentials
```

### **🐳 Setup Infrastruttura**
```bash
# Start Qdrant vector database
docker run -p 6333:6333 qdrant/qdrant

# Start MLflow tracking server
mlflow server --host 127.0.0.1 --port 5001
```

### **▶️ Esecuzione**
```bash
# Metodo principale
python -m src.quiz_generator.main

# Metodo CrewAI CLI
crewai flow kickoff

# Visualizzazione flow
python -c "from src.quiz_generator.main import plot; plot()"
```

### **👤 Esperienza Utente**
```
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

## 📊 Output Files Generati

### **📁 Struttura Output**
```
outputs/
├── 📋 AI_102_document_intelligence_template.md      # Template quiz
├── 📊 AI_102_document_intelligence_questions.json   # Domande JSON
├── 📝 AI_102_document_intelligence_quiz.md          # Quiz vuoto Markdown
├── 📄 AI_102_document_intelligence_quiz.pdf         # Quiz vuoto PDF
├── ✍️ AI_102_document_intelligence_completed_quiz.md # Quiz completato
├── 📄 AI_102_document_intelligence_completed_quiz.pdf # Quiz completato PDF
└── 📊 AI_102_document_intelligence_evaluation.md    # Report valutazione
```

### **📋 Esempio Template**
```markdown
# **Azure - AI_102**

## True/False Questions
1. **[TF_Question_1]**  
  [] True  
  [] False  

## Multiple Choice Questions  
2. **[MC_Question_1]**  
  A) [MC_Option_A_1]  
  B) [MC_Option_B_1]  
  C) [MC_Option_C_1]  
  D) [MC_Option_D_1]  

## Short Open Questions
3. **[Open_Question_1]**  
  ________________________________________________________
```

### **📊 Esempio JSON Questions**
```json
{
  "quiz_info": {
    "topic": "Document Intelligence",
    "certification": "AI_102",
    "provider": "Azure",
    "generated_at": "2025-01-09T10:30:00Z"
  },
  "questions": [
    {
      "id": 1,
      "type": "true_false",
      "question": "Document Intelligence can process only structured documents.",
      "answer": false,
      "explanation": "Document Intelligence can handle both structured and unstructured documents..."
    },
    {
      "id": 2, 
      "type": "multiple_choice",
      "question": "Which service is used for custom document processing?",
      "options": {
        "A": "Form Recognizer",
        "B": "Document Intelligence", 
        "C": "Cognitive Search",
        "D": "Text Analytics"
      },
      "answer": "B",
      "explanation": "Document Intelligence is the updated name for Form Recognizer..."
    }
  ]
}
```

### **🎯 Test Patterns**
```python
def test_quiz_generation():
    """Test generazione quiz AI-900 completa"""
    flow = QuizGeneratorFlow()
    flow.state.provider = "azure"
    flow.state.certification = "AI_900"
    flow.state.topic = "luis"
    
    # Test database initialization
    flow.initialize_vector_database()
    assert flow.state.database_initialized
    
    # Test quiz generation
    flow.generate_quiz_with_rag_crew()
    assert flow.state.quiz_generated
```

## 📊 MLflow Integration & Analytics

### **🔬 Experiment Tracking**
```python
# Configurazione automatica
mlflow.set_tracking_uri("http://127.0.0.1:5001")
mlflow.autolog()
mlflow.set_experiment("FlowGruppo2")
```

### **🧠 LLM Judge Evaluation**
```python
def evaluation_flow():
    """Valutazione automatica con MLflow"""
    eval_metrics = _run_llm_judge_mlflow(
        user_query=question_text,
        prediction=answer,
        context=context,           # opzionale
        ground_truth=ground_truth  # opzionale
    )
    mlflow.log_dict(eval_metrics, "eval_metrics_snapshot.json")
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

## 🔐 Security & Best Practices

### **🔑 Gestione Credenziali**
- ✅ Environment variables per API keys
- ✅ Nessuna persistenza credenziali in codice
- ✅ Rate limiting per API calls
- ✅ Error handling robusto

### **🛡️ Data Privacy**
- ✅ Dataset locale - nessun upload cloud
- ✅ Embedding Azure dedicato
- ✅ Vector database locale (Qdrant)
- ✅ Controllo completo sui dati

### **⚡ Performance Optimization**
- ✅ Collection separate per certificazione
- ✅ Batch processing embedding
- ✅ Connection pooling database
- ✅ Chunking ottimizzato memoria

## 🐛 Troubleshooting

### **❌ Errori Comuni**

**🔧 Database Connection**
```bash
# Start Qdrant se non running
docker run -p 6333:6333 qdrant/qdrant
```

**🔑 Azure OpenAI Configuration**
```bash
# Verifica variabili ambiente
echo $AZURE_OPENAI_API_KEY
echo $AZURE_OPENAI_ENDPOINT
```

**📄 PDF Processing Warnings**
```python
# Warnings automaticamente soppressi in load_pdf()
warnings.filterwarnings("ignore", message=".*Cannot set gray.*")
```

### **🔍 Debug Flow**
```python
# Enable verbose logging
import logging
logging.basicConfig(level=logging.INFO)

# Check state progression
print(f"State: {flow.state}")
```

## 🚀 Roadmap & Estensioni Future

### **🎯 Funzionalità Pianificate**
- 🌍 **Multi-lingua**: Supporto quiz in più lingue
- 🎨 **UI Web**: Interfaccia web per utenti non-tecnici
- 📱 **API REST**: Endpoints per integrazione externa
- 🎓 **Adaptive Learning**: Quiz personalizzati su performance
- 📊 **Advanced Analytics**: Dashboard metriche dettagliate

### **🔧 Miglioramenti Tecnici**
- ⚡ **Parallel Processing**: Generazione parallela domande
- 🔄 **Incremental Updates**: Update incrementali database
- 🎯 **Smart Chunking**: Chunking semantico avanzato

### **🤝 Integrazioni**
- 📱 **Mobile Apps**: App mobile per quiz taking

Il Quiz Generator rappresenta una soluzione completa e scalabile per la generazione automatizzata di quiz educativi, combinando le migliori pratiche di AI, RAG e software engineering in un sistema robusto e user-friendly.
