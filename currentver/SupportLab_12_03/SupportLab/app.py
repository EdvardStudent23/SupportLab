from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_fundraisings.db'
db = SQLAlchemy(app)

class Fundraising(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    credit_number = db.Column(db.String(16), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<users {self.id}>'

@app.route('/', methods=['GET', 'POST'])
def create_fundraising():
    if request.method == 'POST':
        try:
            name = request.form['name']
            credit_number = request.form['credit_number']
            description = request.form['description']
            fundraising = Fundraising(name=name, credit_number=credit_number, description=description)
            db.session.add(fundraising)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"An error occurred: {str(e)}"
    return render_template('createfund.html')

# @app.route('/user_fundraisings')
# def user_fundraisings():
#     fundraisings = Fundraising.query.all() 
#     print(fundraisings)
#     return render_template('userfund.html', fundraisings=fundraisings)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
