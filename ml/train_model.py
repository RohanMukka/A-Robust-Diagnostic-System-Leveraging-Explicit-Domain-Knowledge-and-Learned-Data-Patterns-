import os
import subprocess
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from joblib import dump

DATA_FILE = os.path.join(os.path.dirname(__file__), 'Medical_diagnosis.csv')
KAGGLE_DATASET = 'devdg1/medical-diagnosis'


def load_data():
    if not os.path.exists(DATA_FILE):
        try:
            subprocess.run([
                'kaggle', 'datasets', 'download', '-f', 'Medical_diagnosis.csv', KAGGLE_DATASET,
                '-p', os.path.dirname(DATA_FILE)
            ], check=True)
            import zipfile
            zip_path = DATA_FILE + '.zip'
            if os.path.exists(zip_path):
                with zipfile.ZipFile(zip_path, 'r') as zf:
                    zf.extractall(os.path.dirname(DATA_FILE))
        except Exception as e:
            raise RuntimeError('Dataset not found and kaggle download failed: ' + str(e))
    return pd.read_csv(DATA_FILE)


def preprocess(df):
    X = df.drop('prognosis', axis=1)
    y = df['prognosis']
    return X, y


def train():
    df = load_data()
    X, y = preprocess(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = DecisionTreeClassifier()
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {acc:.2f}')
    print('Confusion matrix:\n', confusion_matrix(y_test, y_pred))
    print('Classification report:\n', classification_report(y_test, y_pred))
    model_path = os.path.join(os.path.dirname(__file__), 'model.joblib')
    dump(clf, model_path)
    return acc


if __name__ == '__main__':
    train()
