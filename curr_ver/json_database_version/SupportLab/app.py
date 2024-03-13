from flask import Flask, render_template, request
import json
import os

app = Flask(__name__)

def load_fundraisings():
    try:
        with open('fundraisings.json', 'r', encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_fundraisings(fundraisings):
    with open('fundraisings.json', 'w', encoding="utf-8") as f:
        json.dump(fundraisings, f, indent=4)

@app.route('/', methods=['GET', 'POST'])
def create_fundraising():
    if request.method == 'POST':
        name = request.form['name']
        credit_number = request.form['credit_number']
        description = request.form['description']
        new_fundraising = {'name': name, 'credit_number': credit_number, 'description': description}
        fundraisings = load_fundraisings()
        fundraisings.append(new_fundraising)
        save_fundraisings(fundraisings)
        return render_template('thanks.html')
    return render_template('createfund.html')
@app.route('/thanks')
def thanks():
    return render_template('thanks.html')
@app.route('/mainpage.html')
def mainpage():
    return render_template('mainpage.html')
@app.route('/topfund.html')
def topfund():
    return render_template('topfund.html')
@app.route('/userfund.html')
def userfund():
    return render_template('userfund.html')
@app.route('/createfund.html')
def createfund():
    return render_template('createfund.html')

if __name__ == '__main__':
    if not os.path.exists('fundraisings.json'):
        with open('fundraisings.json', 'w', encoding="utf-8") as f:
            json.dump([], f)
    app.run(debug=True)
