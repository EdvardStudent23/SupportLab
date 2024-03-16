from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_fundraisings.db'
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 2

db = SQLAlchemy(app)

class Fundraising(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    credit_number = db.Column(db.String(16), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<users {self.id}>'

@app.route('/')
def mainpage():
    return render_template('mainpage.html')

@app.route('/topfund.html')
def topfunds():
    return render_template('topfund.html')

@app.route('/createfund.html', methods=['GET', 'POST'])
def create_fundraising():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        credit_number = request.form['credit_number']
        description = request.form['description']
        
        if len(name) < 3 or len(description) < 10 or len(credit_number) != 16:
            error = 'Your input is wrong! Try again!'
        else:
            try:
                credit_number = ' '.join([credit_number[i:i+4] for i in range(0, len(credit_number), 4)])
                fundraising = Fundraising(name=name, credit_number=credit_number, description=description)
                db.session.add(fundraising)
                db.session.commit()
                return redirect('/userfund.html')
            except Exception as e:
                error = f"An error occurred: {str(e)}"
    return render_template('createfund.html', error=error)

@app.route('/userfund.html')
def userfund():
    fundraisings = Fundraising.query.limit(3).all()
    print(fundraisings)
    return render_template('userfund.html', fundraisings=fundraisings)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)