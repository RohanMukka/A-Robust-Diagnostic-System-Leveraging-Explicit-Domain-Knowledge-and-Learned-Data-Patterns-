from owlready2 import *

onto = get_ontology('http://example.org/medical_ontology.owl')

with onto:
    class Disease(Thing):
        pass
    class Symptom(Thing):
        pass
    class Patient(Thing):
        pass
    class TestResult(Thing):
        pass

    class has_symptom(ObjectProperty):
        domain = [Disease]
        range = [Symptom]
    class patient_has_symptom(ObjectProperty):
        domain = [Patient]
        range = [Symptom]
    class patient_has_history(ObjectProperty):
        domain = [Patient]
        range = [Disease]
    class patient_has_test(ObjectProperty):
        domain = [Patient]
        range = [TestResult]

    class severity(DataProperty):
        domain = [Symptom]
        range = [float]
    class test_value(DataProperty):
        domain = [TestResult]
        range = [float]

    # Predefine common instances used in SWRL rules
    for s in ['Fever', 'Cough', 'ShortnessOfBreath', 'Chills', 'Sweating', 'BodyAche', 'RunnyNose']:
        Symptom(s)
    for d in ['Pneumonia', 'Malaria', 'Flu', 'Diabetes', 'Hypertension']:
        Disease(d)
    for t in ['HighBloodSugar', 'HighBloodPressure']:
        TestResult(t)

onto.save(file = 'ontology/medical_ontology.owl')
