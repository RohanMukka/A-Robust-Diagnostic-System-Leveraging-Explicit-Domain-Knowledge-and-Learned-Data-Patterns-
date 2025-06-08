# A Robust Diagnostic System Leveraging Explicit Domain Knowledge and Learned Data Patterns 

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
