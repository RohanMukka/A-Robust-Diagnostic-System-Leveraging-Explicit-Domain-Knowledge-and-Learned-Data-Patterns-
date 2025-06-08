import os
import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from owlready2 import get_ontology, sync_reasoner_pellet, Imp

ONTO_PATH = os.path.join(os.path.dirname(__file__), '..', 'ontology', 'medical_ontology.owl')
RULES_PATH = os.path.join(os.path.dirname(__file__), '..', 'ontology', 'swr_rules.swrl')


def load():
    onto = get_ontology(ONTO_PATH).load()
    with open(RULES_PATH) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                with onto:
                    Imp().set_as_rule(line)
    return onto


def test_load_ontology():
    load()


def test_swrl_rule_inference():
    onto = load()
    with onto:
        p = onto.Patient('p1')
        p.patient_has_symptom = [onto.Fever, onto.Cough, onto.ShortnessOfBreath]
    sync_reasoner_pellet(infer_property_values=True, infer_data_property_values=True)
    assert onto.Pneumonia in p.patient_has_history
