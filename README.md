# Robust Diagnostic System

This project combines an OWL ontology with SWRL rules and a machine-learning model for disease diagnosis.

## Installation

```bash
pip install owlready2 scikit-learn pandas joblib requests pytest
```

## Training the Model

Download the Kaggle dataset `Medical_diagnosis.csv` into the `ml/` directory or configure Kaggle credentials and run:

```bash
python ml/train_model.py
```

This will train a `DecisionTreeClassifier` and save `ml/model.joblib`.

## Running Diagnosis

Use the CLI tool to diagnose a patient:

```bash
python diagnosis/diagnose.py --symptoms Fever,Cough --tests blood_sugar=140
```

The tool first attempts rule-based reasoning using the ontology and SWRL rules. If no disease is inferred it falls back to the machine‑learning model.

## Adding SWRL Rules

Edit `ontology/swr_rules.swrl` and add new rules in standard SWRL syntax. They will be loaded automatically on the next run.

## Running Tests

```bash
pytest
```

## Deploying on Vercel

Create a Vercel project and push this repository. The serverless API in
`api/diagnose.py` exposes a `/api/diagnose` endpoint. Vercel automatically
installs `requirements.txt` and serves the Flask app. Pass symptoms and optional
tests via JSON or query parameters:

```bash
curl -G https://your-vercel-deployment.vercel.app/api/diagnose \
    --data-urlencode "symptoms=Fever,Cough"
```

The response will contain either the rule-based or machine-learning diagnosis.
