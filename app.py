from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('coffee_shop.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_name TEXT,
                    coffee TEXT,
                    quantity INTEGER,
                    bakery TEXT,
                    coffee_price REAL,
                    bakery_price REAL,
                    total REAL
                )''')
    conn.commit()
    conn.close()


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        name = request.form['customer_name']
        coffee = request.form['coffee']
        qty = int(request.form['quantity'])
        bakery = request.form['bakery']

        # coffee & bakery prices (example rates)
        coffee_prices = {
        "Espresso": 100,
        "Cappuccino": 150,
        "Americano": 110,
        "Vanilla Latte": 170,
        "Hot Chocolate": 130,
        "Turmeric Latte": 175,
        "Iced Coffee": 120,
        "Venilla Cold FOam": 170,
        "Cold Brew": 150,
        "Iced Latte": 140,
        "Mocha Frappe": 190,
        "Caramel Iced Latte": 180,
        "Oreo Frappe": 200,
        "Choco Mint Cold Brew": 185,

        }
        bakery_prices = {
            "Croissant": 80,
            "Muffin": 70,
            "Donut": 60,
            "Cinnamon Roll": 95,
            "Butter Biscuit": 65,
            "Chocolate Chip Cookie": 95,
            "Banana Bread": 85,
            "Cheese Danish": 100,
            "None": 0,
        }



        coffee_price = coffee_prices.get(coffee, 0)
        bakery_price = bakery_prices.get(bakery, 0)

        total = (coffee_price * qty) + bakery_price


        return render_template('confirm.html',
                               name=name,
                               coffee=coffee,
                               qty=qty,
                               coffee_price=coffee_price,
                               bakery=bakery,
                               bakery_price=bakery_price,
                               total=total)
    return render_template('order.html')


@app.route('/confirm', methods=['POST'])
def confirm():
    name = request.form['name']
    coffee = request.form['coffee']
    qty = int(request.form['qty'])
    bakery = request.form['bakery']
    coffee_price = float(request.form['coffee_price'])
    bakery_price = float(request.form['bakery_price'])
    total = float(request.form['total'])

    conn = sqlite3.connect('coffee_shop.db')
    c = conn.cursor()
    c.execute('''INSERT INTO orders (customer_name, coffee, quantity, bakery, coffee_price, bakery_price, total)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (name, coffee, qty, bakery, coffee_price, bakery_price, total))
    conn.commit()
    conn.close()

    return render_template('bill.html',
                           name=name,
                           coffee=coffee,
                           qty=qty,
                           bakery=bakery,
                           coffee_price=coffee_price,
                           bakery_price=bakery_price,
                           total=total)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
