from flask import Flask, render_template, request, redirect, url_for
from main import extract_text_from_pdf, process_book, ask_question
import os

app = Flask(__name__, static_folder='frontend', template_folder='frontend')

# Global
book_name = ""

# Homepage
@app.route('/', methods=['GET', 'POST'])
def index():
    global book_name
    if request.method == 'POST':
        if 'pdf' not in request.files:
            return redirect(request.url)

        file = request.files['pdf']
        if file.filename == '':
            return redirect(request.url)

        if file:
            book_name = file.filename 
            text = extract_text_from_pdf(file)
            process_book(text)
            return redirect(url_for('ask'))

    return render_template('index.html')

# Asking questions
@app.route('/ask', methods=['GET', 'POST'])
def ask():
    global book_name
    if request.method == 'POST':
        question = request.form['question']

        answer = ask_question(question)
        return render_template('ask.html', question=question, answer=answer, book_name=book_name)

    return render_template('ask.html', question=None, answer=None, context=None, book_name=book_name, exit=False)

# Exit button
@app.route('/exit', methods=['POST'])
def exit_app():
    return render_template('ask.html', question=None, answer=None, context=None, book_name=book_name, exit=True)

if __name__ == '__main__':
    app.run(debug=True)