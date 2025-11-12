# Dumroo.ai – Role-Based AI Query System (Ollama + Streamlit)

## Features
- Admin login with role-based data filtering
- Dynamic data loading (all CSVs in `data/`)
- Local LLM integration (Ollama + LangChain)
- Query data using natural language
- Works fully offline!

## Setup
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Start Ollama:
```bash
ollama serve
ollama list
```

Then run the app:
```bash
python -m streamlit run app.py
```
