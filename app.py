from urllib import request
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text


app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/database_name'
#db = SQLAlchemy(app)

@app.route('/')
def hello_world():  
    return render_template('index.html')

@app.route('/search.html')
def search():
    return render_template('search.html')

@app.route('/manual_search.html')
def manual_search():
    return render_template('manual_search.html')

@app.route('/book.html')
def manual_search():
    return render_template('book.html')


@app.route('/gosearch.html')
def manual_search():
    return render_template('gosearch.html')


@app.route('/clientLogin.html')
def manual_search():
    return render_template('clientLogin.html')

@app.route('/clientSignUp.html')
def manual_search():
    return render_template('clientSignUp.html')

@app.route('/employeeLogin.html')
def manual_search():
    return render_template('employeeLogin.html')

@app.route('/employeeSignUp.html')
def manual_search():
    return render_template('employeeSignUp.html')


#class Product(db.Model):
 #   id = db.Column(db.Integer, primary_key=True)
  #  name = db.Column(db.String(100), nullable=False)
   # description = db.Column(db.String(200))
    #price = db.Column(db.Float)

#@app.route('/search', methods=['GET'])
#def search():
#    amenities = request.args.get('amenities')
 #   pricehigh = request.args.get('pricehigh')
  #  pricelow = request.args.get('pricelow')
   # extendible = request.args.get('extendible')

    # Start building the SQL query
#    sql_query = "SELECT * FROM products WHERE 1=1"
#
 #   if amenities:
  #      sql_query += f" AND amenities ILIKE '%{amenities}%'"
   # if pricehigh:
    #    sql_query += f" AND price <= {pricehigh}"
#    if pricelow:
 #       sql_query += f" AND price >= {pricelow}"
  #  if extendible:
   #     sql_query += f" AND extendible = '{extendible}'"
    
    #sql_query += f" AND isAvailable = 'TRUE'"

    # Execute
#    results = db.session.execute(text(sql_query))

    # Format results
#    html_results = ''
 #   for row in results:
  #      html_results += f'<div class="room">'
   #     html_results += f'<img src="{row.image}" alt="{row.name}">'
    #    html_results += f'<div class="details">'
     #   html_results += f'<h2>{row.name}</h2>'
#        html_results += f'<p>Price: ${row.price} per night</p>'
 #       html_results += f'<button class="book-button" onclick="booked({row.RoomID})"><a href="book.html">Book</a></button>' #also make clicking this take the user to another page, keeping track of the specific room id they chose
  #      html_results += f'</div>'
   #     html_results += f'</div>'
    
    #return html_results

if __name__ == '__main__':
    app.run()