from flask import Flask, request, jsonify
from diagnosis.diagnose import diagnose

app = Flask(__name__)

@app.route('/api/diagnose', methods=['GET', 'POST'])
def handle():
    data = request.get_json(silent=True) or {}
    symptoms = data.get('symptoms') or request.args.get('symptoms', '')
    tests_param = data.get('tests') or request.args.get('tests', '')

    symptoms_list = [s.strip() for s in str(symptoms).split(',') if s.strip()]
    tests = {}
    if isinstance(tests_param, dict):
        tests = {k: v for k, v in tests_param.items()}
    else:
        for pair in str(tests_param).split(','):
            if '=' in pair:
                k, v = pair.split('=', 1)
                tests[k.strip()] = v.strip()

    result = diagnose(symptoms_list, tests)
    return jsonify(result)

# Vercel looks for a variable named "app" or a handler function
handler = app
