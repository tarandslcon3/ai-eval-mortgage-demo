# Northfield Harbour Mortgage Assistant — Evaluation Demo

> **SYNTHETIC DATA — all documents, lender names, rates, and policies are entirely fictional and invented for AI evaluation purposes. This is not financial advice and does not represent any real lender.**

## Purpose

This project is a small RAG (retrieval-augmented generation) assistant built over synthetic mortgage policy documents for a fictional lender, Northfield Harbour Lending. It is intended for evaluating AI assistant quality and robustness.

## Run the CLI

```bash
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt   # Windows
# or: .venv/bin/pip install -r requirements.txt  # macOS/Linux

cp .env.example .env
# Add your ANTHROPIC_API_KEY to .env

python -m assistant "What is the minimum down payment for a $600,000 home?"
```

## Run the API

```bash
uvicorn api:app --port 8000
# POST http://localhost:8000/ask
# Body: {"question": "What is the minimum credit score?"}
```

## Project Structure

```
docs/           Synthetic mortgage policy documents
assistant/      RAG assistant package (corpus, retrieval, bot)
api.py          FastAPI service
.env.example    Environment variable template
```

## Disclaimer

Northfield Harbour Lending is a fictional entity created for this demo. All rates, thresholds, fees, and policies are invented. Do not use any information from this project as mortgage or financial advice.
