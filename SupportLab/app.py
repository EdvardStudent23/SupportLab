from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_fundraisings.db'
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 2

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Fundraising(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    _credit_number = db.Column(db.String(16), unique=True, nullable=False)  # Store as continuous string
    description = db.Column(db.Text, nullable=False)

    @property
    def credit_number(self):
        # Format credit number for display
        return ' '.join([self._credit_number[i:i+4] for i in range(0, len(self._credit_number), 4)])

    @credit_number.setter
    def credit_number(self, value):
        # Remove whitespace and store as continuous string
        self._credit_number = ''.join(value.split())

@app.route('/')
def mainpage():
    return render_template('mainpage.html')

@app.route('/topfund.html')
def topfunds():
    return render_template('topfund.html')
@app.route('/mainpage.html')
def mainpage_reference():
    return render_template('mainpage.html')
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
                # credit_number = ' '.join([credit_number[i:i+4] for i in range(0, len(credit_number), 4)])
                fundraising = Fundraising(name=name, _credit_number=credit_number, description=description)
                db.session.add(fundraising)
                db.session.commit()
                return redirect('/userfund.html')
            except Exception as e:
                error = f"An error occurred: {str(e)}"
    return render_template('createfund.html', error=error)

@app.route('/userfund.html')
def userfund():
    page = request.args.get('page', 1, type=int)
    per_page = 3  # Number of items per page

    fundraisings = Fundraising.query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('userfund.html', fundraisings=fundraisings)

if __name__ == '__main__':
    with app.app_context():
        # db.drop_all()
        db.create_all()
    app.run(debug=True)
