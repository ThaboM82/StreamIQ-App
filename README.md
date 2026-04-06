# StreamIQ – Real-Time Customer Intelligence 🚀

[![CI/CD Pipeline](https://github.com/ThaboM82/streamiq/actions/workflows/github_actions.yml/badge.svg)]()
[![Coverage Status](https://img.shields.io/badge/coverage-90%25-brightgreen.svg)]()
[![Docker Build](https://img.shields.io/badge/docker-ready-green.svg)]()
[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)]()
[![AWS ECS](https://img.shields.io/badge/deploy-ecs-orange.svg)]()

---

## 📖 Overview
**StreamIQ** is a modular, scalable NLP pipeline for **real-time customer intelligence** in banks, insurers, and call centers.  

It integrates:
- 🎙️ Speech-to-Text transcription  
- 🧠 NLP (sentiment + intent classification)  
- 📊 Satisfaction prediction  
- 🗄️ MySQL persistence with Alembic migrations  
- 📈 Recruiter-facing Streamlit dashboard  
- 🔄 Full MLOps discipline with **MLflow** + **DVC**  
- 🐳 Docker + ECS deployment with CI/CD automation  
- ⚡ Dual NLP engines: **Spark NLP (big data)** + **Hugging Face (demo mode)**  

---

## 🛠️ Tech Stack
- **Python 3.11**
- **Flask** – REST API endpoints
- **Streamlit** – dashboards
- **PySpark + Spark NLP** – scalable big data NLP
- **Hugging Face Transformers** – lightweight demo NLP
- **MySQL + SQLAlchemy + Alembic** – persistence + migrations
- **Docker + ECS** – deployment
- **GitHub Actions** – CI/CD automation
- **MLflow** – experiment tracking
- **DVC** – dataset + model versioning
- **Pytest** – unit + integration tests

---

## ⚡ Big Data Mode vs Demo Mode

StreamIQ supports **dual NLP engines**:

- **Big Data Mode (Spark NLP)**  
  Run distributed pipelines with PySpark + Spark NLP.  
  ```bash
  export NLP_ENGINE=spark
  python src/app.py

Demo Mode (Hugging Face)  
Lightweight mode for demos and local testing.

Bash

export NLP_ENGINE=hf
python src/app.py

📂 Project Structure
StreamIQ/
│── README.md
│── requirements.txt
│── Dockerfile
│── docker-compose.yml
│── pyproject.toml
│── setup.cfg
│── setup.py
│
├── src/
│   ├── __init__.py
│   ├── app.py             # Flask entry point
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py      # API endpoints
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── models.py      # SQLAlchemy ORM models
│   │   └── connection.py  # Database connection setup
│   │
│   ├── speech_to_text/
│   │   ├── __init__.py
│   │   └── transcriber.py # Speech-to-text engine
│   │
│   ├── nlp/
│   │   ├── __init__.py
│   │   ├── sentiment.py   # Sentiment analysis
│   │   └── intent.py      # Intent classification
│   │
│   ├── satisfaction/
│   │   ├── __init__.py
│   │   └── predictor.py   # Satisfaction scoring
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── helpers.py     # Text cleaning, timestamp formatting
│   │   ├── logger.py      # Centralized logging
│   │   └── validators.py  # Payload validation
│   │
│   └── tests/
│       ├── __init__.py
│       ├── test_api.py        # Tests for API routes
│       ├── test_predictor.py  # Tests for satisfaction predictor
│       ├── test_sentiment.py  # Tests for sentiment analysis
│       └── test_transcriber.py# Tests for speech-to-text
│
├── dashboards/
│   ├── __init__.py
│   └── streamlit_app.py   # Streamlit dashboard
│
├── ci_cd/
│   └── github_actions.yml # CI/CD pipeline config
│
├── ecs/
│   └── task_definition.json # AWS ECS task definition
│
├── mlflow/
│   ├── experiments/       # Experiment tracking
│   └── config.yml
│
├── dvc/
│   ├── data/
│   │   ├── raw/           # Raw datasets
│   │   └── processed/     # Processed datasets
│   ├── models/            # Versioned models
│   └── dvc.yaml           # DVC pipeline config
│
└── demo/
    ├── demo_predict.py    # Demo satisfaction prediction
    └── demo_transcribe.py # Demo speech-to-text
│
└── LICENSE                # MIT License © 2026 Percy Thabo Mathebula

▶️ Launch the Dashboard
Powershell
streamlit run dashboards/streamlit_app.py

The app will open at http://localhost:8501.

🛠️ Troubleshooting

ModuleNotFoundError: No module named 'src'
Ensure you’re running from the project root (C:\StreamIQ App).

Verify __init__.py exists in src/ and its subfolders.

Add PYTHONPATH to your venv activation script:

$env:PYTHONPATH="C:\StreamIQ App"

Streamlit not opening in browser
Check if the app is running at http://localhost:8501.

If blocked, open manually in your browser


## 🚀 Deployment

StreamIQ is designed with an **enterprise‑grade CI/CD pipeline** that ensures every commit is tested, containerized, and ready for production deployment.

### 🔹 CI/CD Workflow
- **GitHub Actions** (`ci_cd/github_actions.yml`) runs automatically on every push and pull request.
- Pipeline stages:
  1. **Linting** → `flake8` enforces code quality.
  2. **Testing** → `pytest` validates functionality.
  3. **Docker Build** → container image built locally and in CI.
  4. **Artifact Upload** → coverage reports and logs stored for review.
  5. **Deployment (future)** → automatic push to AWS ECS once credentials and cluster are configured.

### 🔹 Deployment Targets
- **Local Development**  
  Run StreamIQ in Docker:
  ```bash
  docker build -t streamiq-app .
  docker run -p 8501:8501 streamiq-app


