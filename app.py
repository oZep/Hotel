from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime
import psycopg2 as pg

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:issadogs@localhost/hotel'
db = SQLAlchemy(app)


# Connect to the database 
conn = pg.connect(database="hotel", user="postgres", 
                        password="issadogs", host="localhost", port="5432") 
  
# create a cursor 
cur = conn.cursor() 
  

class Room(db.Model):
    __tablename__ = 'room'

    room_id = db.Column(db.Integer, primary_key=True)
    capacity = db.Column(db.Integer)
    extendable = db.Column(db.Boolean)
    hotel_id = db.Column(db.Integer)
    isavailable = db.Column(db.Boolean)
    price = db.Column(db.Numeric)
    view = db.Column(db.Boolean)

class Book(db.Model):
    __tablename__ = 'book'

    ba_id = db.Column(db.Integer, primary_key=True)
    cus_id = db.Column(db.Integer, db.ForeignKey('customer.cus_id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.room_id'))

class Customer(db.Model):
    __tablename__ = 'customer'

    cus_id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(255))
    address = db.Column(db.String(255))
    registrationdate = db.Column(db.Date)

# Define the Employee class
class Employee(db.Model):
    __tablename__ = 'employee'

    ssn = db.Column(db.Integer, primary_key=True)
    hotel_id = db.Column(db.Integer)
    role = db.Column(db.String)
    name = db.Column(db.String)
    address = db.Column(db.String)

    def print(self):
        employees = Employee.query.all()
        for employee in employees:
            print(f"Name: {employee.name}, SSN: {employee.ssn}")

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

@app.route('/employee_page')
def employee_page():
    # Query the database to get information for each booking
    bookings = db.session.query(
        Book.ba_id,
        Customer.fullname.label('client_name'),
        Customer.registrationdate.label('check_in_date'),
        Room.room_id
    ).join(Customer, Book.cus_id == Customer.cus_id).join(Room, Book.room_id == Room.room_id).all()

    print(bookings)
    print("Hi")

    # Render the template with the bookings information
    return render_template('employeePage.html', reservations=bookings)

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


@app.route('/print_employees')
def print_employees():
    with app.app_context():
        employee_instance = Employee()
        employee_instance.print()
    return 'Employee information printed in the console.'


@app.route('/signin', methods=['POST'])
def signin():
    username = request.form['name']
    password = request.form['ssn']
    
    # Query the database to check if the provided username and password match any entry in the employee table
    employee = Employee.query.filter_by(name=username, ssn=password).first()

    # some employee names to test
    # Name: John Doe, SSN: 123456789
    # Name: Jane Smith, SSN: 987654321
    # Name: Olivia Brown, SSN: 569779378
    # Name: Emma Jones, SSN: 15158238
    # Name: William Williams, SSN: 280896680
    # Name: Olivia Davis, SSN: 943821732
    # Name: Emma Garcia, SSN: 642517885
    # Name: Emma Williams, SSN: 118782618
    # Name: John Jones, SSN: 400805752

    if employee:
        # Authentication successful, redirect to employee page
        return redirect(url_for('employee_page'))
    else:
        # Authentication failed, redirect back to sign-in page
        return redirect(url_for('employee_signup'))



@app.route('/search', methods=['GET'])
def search():
    amenities = request.args.get('amenities')
    pricelow = request.args.get('pricelow')
    pricehigh = request.args.get('pricehigh')
    rating = request.args.get('rating')
    extendible = request.args.get('extendible')

    query = Room.query

    if amenities:
        query = query.filter(Room.amenities.ilike(f"%{amenities}%"))

    if pricelow:
        query = query.filter(Room.price >= pricelow)

    if pricehigh:
        query = query.filter(Room.price <= pricehigh)

    if rating:
        # Add filtering based on rating
        query = query.filter(Room.rating == rating)

    if extendible == 'on':
        query = query.filter(Room.extendable == True)
    else:
        query = query.filter(Room.extendable == False)

    results = query.all()

    return render_template('search_results.html', results=results)


@app.route('/book/<int:room_id>', methods=['GET', 'POST'])
def book_room(room_id):
    # Render the booking page template
    current_date = datetime.now().strftime('%Y-%m-%d')
    room_id = room_id
    return render_template('book.html', room_id=room_id, current_date=current_date)


@app.route('/submit_booking/<int:room_id>', methods=['POST'])
def submit_booking(room_id):
    # Extract information from the booking form
    room_id_from_form = request.form.get('room_id')
    fullname = request.form.get('fullname')
    address = request.form.get('address')
    dateofreg = request.form.get('dateofreg')

    # Insert the new customer into the database
    cur = conn.cursor()
    cur.execute("INSERT INTO customer (cus_id, fullname, address, registrationdate) VALUES (%s, %s, %s, %s) RETURNING cus_id", (room_id, fullname, address, dateofreg))
    new_customer_id = cur.fetchone()[0]
    conn.commit()

    # Update the room's availability
    cur.execute("UPDATE room SET isavailable = FALSE WHERE room_id = %s", (room_id,))
    conn.commit()

    # Optionally, add entry to the book table
    cur.execute("INSERT INTO book (cus_id, room_id) VALUES (%s, %s)", (new_customer_id, room_id))
    conn.commit()

    # Redirect to a confirmation page or render confirmation message
    return render_template('confirmation.html', customer=room_id, room_id=room_id)


if __name__ == '__main__':
    app.run(debug=True)


   # Create a new Customer instance
        #new_customer = Customer(fullname=fullname, address=address, registrationdate=datetime.strptime(dateofreg, '%Y-%m-%d').date())

        # Add the new customer to the database
        #db.session.add(new_customer)
        #db.session.commit()

        # Update the room's availability
        #room = Room.query.get(room_id)
        #room.isavailable = False
        #db.session.commit()