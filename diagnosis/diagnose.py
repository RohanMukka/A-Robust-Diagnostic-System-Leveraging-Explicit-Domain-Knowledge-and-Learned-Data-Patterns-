import argparse
import os
from owlready2 import get_ontology, sync_reasoner_pellet, Imp
import joblib
import pandas as pd

ONTOLOGY_PATH = os.path.join(os.path.dirname(__file__), '..', 'ontology', 'medical_ontology.owl')
RULES_PATH = os.path.join(os.path.dirname(__file__), '..', 'ontology', 'swr_rules.swrl')
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'ml', 'model.joblib')
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'ml', 'Medical_diagnosis.csv')


def load_ontology():
    onto = get_ontology(ONTOLOGY_PATH).load()
    with open(RULES_PATH) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                with onto:
                    Imp().set_as_rule(line)
    return onto


def run_reasoner(onto, symptoms, tests):
    with onto:
        patient = onto.Patient('temp_patient')
        for s in symptoms:
            symptom_cls = onto.search_one(iri='*#' + s)
            if symptom_cls is None:
                symptom_cls = onto.Symptom(s)
            patient.patient_has_symptom.append(symptom_cls)
        for tname, val in tests.items():
            test_cls = onto.search_one(iri='*#' + tname)
            if test_cls is None:
                test_cls = onto.TestResult(tname)
            tr = test_cls()
            tr.test_value = float(val)
            patient.patient_has_test.append(tr)
        sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
        diseases = list(patient.patient_has_history)
        for inst in patient.patient_has_symptom: pass
    return diseases


def ml_diagnosis(symptoms):
    clf = joblib.load(MODEL_PATH)
    df = pd.read_csv(DATA_PATH)
    feature_cols = df.drop('prognosis', axis=1).columns
    input_data = {col: 0 for col in feature_cols}
    for s in symptoms:
        if s in input_data:
            input_data[s] = 1
    X = pd.DataFrame([input_data])
    pred = clf.predict(X)[0]
    return pred


def diagnose(symptoms, tests):
    """Run diagnosis using rules then ML fallback."""
    onto = load_ontology()
    diseases = run_reasoner(onto, symptoms, tests)
    if diseases:
        return {
            'method': 'rule',
            'diseases': [d.name for d in diseases]
        }
    pred = ml_diagnosis(symptoms)
    return {
        'method': 'ml',
        'disease': pred
    }


def main():
    parser = argparse.ArgumentParser(description='Diagnostic CLI')
    parser.add_argument('--symptoms', required=True, help='Comma separated symptoms')
    parser.add_argument('--tests', default='', help='Comma separated test=value pairs')
    args = parser.parse_args()

    symptoms = [s.strip() for s in args.symptoms.split(',') if s.strip()]
    tests = {}
    for pair in args.tests.split(','):
        if '=' in pair:
            k,v = pair.split('=',1)
            tests[k.strip()] = v.strip()

    result = diagnose(symptoms, tests)
    if result['method'] == 'rule':
        print('Rule-based diagnosis:', ', '.join(result['diseases']))
    else:
        print('ML-based diagnosis:', result['disease'])


if __name__ == '__main__':
    main()
