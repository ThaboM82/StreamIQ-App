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
│   ├── app.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py        # Flask API endpoints
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── models.py        # SQLAlchemy ORM models
│   │   └── connection.py    # MySQL connection setup
│   │
│   ├── speech_to_text/
│   │   ├── __init__.py
│   │   └── transcriber.py
│   │
│   ├── nlp/
│   │   ├── __init__.py
│   │   ├── sentiment.py
│   │   └── intent.py
│   │
│   ├── satisfaction/
│   │   ├── __init__.py
│   │   └── predictor.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logger.py
│   │
│   └── tests/               # ✅ New test suite
│       ├── __init__.py
│       ├── test_transcriber.py
│       ├── test_sentiment.py
│       ├── test_predictor.py
│       └── test_api.py
│
├── dashboards/
│   ├── __init__.py
│   └── streamlit_app.py     # ✅ Polished dashboard
│
├── ci_cd/
│   └── github_actions.yml
│
├── ecs/
│   └── task_definition.json
│
├── mlflow/
│   ├── experiments/
│   └── config.yml
│
├── dvc/
│   ├── data/
│   │   ├── raw/             # ✅ Sample dataset
│   │   └── processed/
│   ├── models/
│   └── dvc.yaml
│
└── demo/                    # ✅ Recruiter demo scripts
    ├── demo_predict.py
    └── demo_transcribe.py

📜 License
MIT License © 2026 Percy Thabo Mathebula