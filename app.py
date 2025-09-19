from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///real_estate.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model to represent properties
class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    available = db.Column(db.Boolean, default=True)

# Route to the home page where properties are listed
@app.route('/')
def home():
    properties = Property.query.filter_by(available=True).all()
    return render_template('home.html', properties=properties)

# Route to add a property
@app.route('/add_property', methods=['GET', 'POST'])
def add_property():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        price = request.form['price']
        
        new_property = Property(name=name, location=location, price=float(price))
        db.session.add(new_property)
        db.session.commit()
        
        return redirect(url_for('home'))
    
    return render_template('add_property.html')

# Route to book a property
@app.route('/book_property/<int:property_id>', methods=['GET'])
def book_property(property_id):
    property_to_book = Property.query.get_or_404(property_id)
    property_to_book.available = False
    db.session.commit()
    return redirect(url_for('home'))

# Initialize the database
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
