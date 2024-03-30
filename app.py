from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime

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

@app.route('/search_results.html')
def search_results():
    return render_template('search_results.html')

@app.route('/confirmation/<int:room_id>/<int:customer_id>')
def confirmation(room_id, customer_id):
    # Retrieve customer and room information
    customer = Customer.query.get(customer_id)
    room = Room.query.get(room_id)
    return render_template('confirmation.html', customer=customer, room_id=room_id)


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

class Room(db.Model):
    __tablename__ = 'room'

    room_id = db.Column(db.Integer, primary_key=True)
    capacity = db.Column(db.Integer)
    extendable = db.Column(db.Boolean)
    hotel_id = db.Column(db.Integer)
    isavailable = db.Column(db.Boolean)
    price = db.Column(db.Numeric)
    view = db.Column(db.Boolean)

class Customer(db.Model):
    __tablename__ = 'customer'

    cus_id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(255))
    address = db.Column(db.String(255))
    registrationdate = db.Column(db.Date)


@app.route('/search', methods=['GET'])
def search():
    amenities = request.args.get('amenities')
    pricelow = request.args.get('pricelow')
    pricehigh = request.args.get('pricehigh')
    extendible = request.args.get('extendible')
    view = request.args.get('view')

    query = Room.query

    # Filter based on search parameters
    if amenities:
        query = query.filter(Room.amenities.ilike(f"%{amenities}%"))
    if pricelow:
        query = query.filter(Room.price >= float(pricelow))
    if pricehigh:
        query = query.filter(Room.price <= float(pricehigh))
    if extendible:
        query = query.filter(Room.extendible == True)
    if view:
        query = query.filter(Room.view == True)

    results = query.all()

    return render_template('search_results.html', results=results)


@app.route('/book/<int:room_id>', methods=['GET', 'POST'])
def book_room(room_id):
    if request.method == 'POST':
        # Extract information from the booking form
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        address = request.form.get('address')
        dateofreg = request.form.get('dateofreg')

        # Create a new Customer instance
        new_customer = Customer(fullname=fullname, address=address, registrationdate=datetime.strptime(dateofreg, '%Y-%m-%d').date())

        # Add the new customer to the database
        db.session.add(new_customer)
        db.session.commit()

        # Update the room's availability
        room = Room.query.get(room_id)
        room.isavailable = False
        db.session.commit()

        # Redirect to a confirmation page or somewhere else
        return redirect(url_for('confirmation', room_id=room_id, customer_id=new_customer.id))

    # Render the booking page template
    return render_template('book.html', room_id=room_id)

if __name__ == '__main__':
   app.run(debug=True)