from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:issadogs@localhost/hotel'
db = SQLAlchemy(app)

# Dummy user data for demonstration
users = {'user1': 'password1', 'user2': 'password2'}

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/searchS.html')
def search_page():
    return render_template('searchS.html')

@app.route('/manual_search.html')
def manual_search():
    return render_template('manual_search.html')

@app.route('/book.html')
def book():
    return render_template('book.html')

@app.route('/gosearch.html')
def gosearch():
    return render_template('gosearch.html')

@app.route('/clientSignUp.html')
def client_signup():
    return render_template('clientSignUp.html')

@app.route('/employeeSignUp.html')
def employee_signup():
    return render_template('employeeSignUp.html')

@app.route('/employeePage.html')
def employee_page():
    return render_template('employeePage.html')

@app.route('/employee')
def employee():
    return render_template('employeePage.html')

@app.route('/signin', methods=['POST'])
def signin():
    username = request.form['name']
    password = request.form['ssn']
    
    if username in users and users[username] == password:
        # Authentication successful, redirect to employee page
        return redirect(url_for('employee_page'))
    else:
        # Authentication failed, redirect back to sign-in page
        return redirect(url_for('employee_signup'))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)

@app.route('/search', methods=['GET'])
def search():
    amenities = request.args.get('amenities')
    price_high = request.args.get('pricehigh')
    price_low = request.args.get('pricelow')
    extendible = request.args.get('extendible')

    # Start building the SQL query using parameterized query
    query = Product.query.filter_by(isAvailable=True)
    if amenities:
        query = query.filter(Product.amenities.ilike(f'%{amenities}%'))
    if price_high:
        query = query.filter(Product.price <= float(price_high))
    if price_low:
        query = query.filter(Product.price >= float(price_low))
    if extendible:
        query = query.filter(Product.extendible == extendible)

    # Execute the query
    results = query.all()

    # Render template with search results
    return render_template('search_results.html', results=results)

if __name__ == '__main__':
    app.run()
