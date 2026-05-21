from setuptools import setup, find_packages

setup(
    name="streamiq",
    version="0.1.0",
    description="StreamIQ modular NLP pipeline and dashboards",
    author="Percy",
    author_email="thabo.math@icloud.com",
    url="https://github.com/ThaboM82/Streamiq-App",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    python_requires=">=3.11",
    install_requires=[
        # Core frameworks
        "flask>=3.0.0",
        "streamlit>=1.32.0",
        "streamlit-autorefresh>=1.0.0",

        # Data science stack
        "numpy>=1.26.0",
        "pandas>=2.2.0",
        "scikit-learn==1.4.1.post1",
        "sqlalchemy>=2.0.0",
        "alembic==1.13.1",

        # HTTP & config
        "requests>=2.31.0",
        "python-decouple==3.8",
        "python-dotenv>=1.0.0",
        "pydantic>=2.6.0",

        # NLP modules
        "nltk>=3.8.1",
        "transformers>=4.39.0",
        "spacy==3.8.14",
        "en-core-web-sm==3.8.0",
        "spark-nlp==5.3.0",
        "textblob>=0.17.1",
        "langdetect>=1.0.9",

        # Speech-to-text
        "speechrecognition>=3.10.0",
        "openai-whisper>=20231117",

        # Workflow & MLOps
        "mlflow>=2.11.0,<3.0",
        "dvc>=3.49.0,<4.0",
        "docker==7.0.0",

        # Visualization
        "plotly==5.19.0",
        "matplotlib==3.8.3",
        "seaborn==0.13.2",
        "altair>=5.0.0",

        # Document generation
        "fpdf2>=2.7.8",
        "xlsxwriter>=3.2.0",

        # Testing & CI/CD
        "pytest==8.1.1",
        "pytest-cov==5.0.0",
        "coverage==7.4.4",

        # Big data / ML
        "pyspark==3.5.1",
        "torch==2.2.2",

        # Database drivers
        "mysqlclient==2.2.4",

        # Automated ML benchmarking
        "pycaret==3.0.0",

        # Interactive dev
        "ipython>=8.20.0",
    ],
    extras_require={
        "dev": [
            "jupyterlab>=4.1.0",
            "black==24.4.0",
            "isort==5.13.2",
            "pre-commit>=3.7.0",
        ],
        "ml": [
            "pycaret==3.0.0",
            "spark-nlp==5.3.0",
            "torch==2.2.2",
        ],
        "docs": [
            "sphinx>=7.0.0",
            "sphinx-rtd-theme>=1.3.0",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "Framework :: Streamlit",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
    ],
)
