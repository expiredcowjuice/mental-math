from flask import Flask, jsonify, request, render_template
import random

app = Flask(__name__)

questions = []  # Store questions and answers
current_score = {'correct': 0, 'attempted': 0}

@app.route('/')
def home():
    global questions
    questions = []  # Reset questions for a new session
    global current_score
    current_score = {'correct': 0, 'attempted': 0}  # Reset score
    return render_template('index.html')

def generate_question():
    x = random.randint(2, 20)  # Ensure x > 1 for valid fractions
    y = random.randint(1, x-1)
    question = f"{y}/{x}"
    answer = round(y/x, 5)  # Adjust precision as needed
    questions.append({'question': question, 'answer': answer})
    return {'question': question, 'id': len(questions) - 1}

@app.route('/get_question', methods=['GET'])
def get_question():
    question = generate_question()
    return jsonify(question)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.json
    question_id = data['id']
    user_answer = float(data['answer'])
    correct_answer = questions[question_id]['answer']

    global current_score
    current_score['attempted'] += 1
    if abs(user_answer - correct_answer) < 0.0001:  # Allow small margin of error
        current_score['correct'] += 1
        return jsonify({'correct': True})
    else:
        return jsonify({'correct': False, 'right_answer': correct_answer})

@app.route('/get_score', methods=['GET'])
def get_score():
    return jsonify(current_score)

@app.route('/reset_score', methods=['POST'])
def restart():
    global questions
    questions = []
    global current_score
    current_score = {'correct': 0, 'attempted': 0}

if __name__ == '__main__':
    app.run(debug=True)
