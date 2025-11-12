# Dumroo.ai – Role-Based AI Query System (Ollama + Streamlit)

## Features
- Admin login with role-based data filtering
- 3 types of users each with unique privileges
    Principal: Has full access to all student records and AI querying across every region.
    Teacher(admin1& admin2): Can view and query only the students assigned to their class, grade, or region.
- Dynamic data loading (all CSVs in `data/`)
- Local LLM integration (Ollama + LangChain)
- Query data using natural language
- Works fully offline!

## 🧩 Tech Stack

| Component | Technology Used |
|------------|-----------------|
| Frontend | Streamlit |
| Backend | Python |
| AI Engine | LangChain + Ollama |
| Data Handling | Pandas |
| Auth Storage | JSON-based (admins.json) |


## Setup
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
Install Ollama
Start Ollama:
```bash
ollama serve
ollama list
```

Then run the app:
```bash
python -m streamlit run app.py
```
