from flask import Flask, request, render_template, session, redirect, url_for, jsonify
import user_service as us
import customer_service as cs
import order_service as os
import re

app = Flask(__name__)
app.secret_key = b'I9e0n6_2w2q'

@app.route('/', methods=['GET'])
def index():
    if 'email' in session:
        username = us.get_name_by_email(session['email'])
        return render_template('starter.html', email=session['email'], username=username, title="Dashboard", active_parent="Dashboard", active_function="dashboard")
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form['email']
        password = request.form['password']
        if us.check_email_password(email, password):
            session['email'] = email
            return '0'
        else:
            return '1'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            return '1'
        elif len(password) < 8:
            return '2'
        elif username == "":
            return '3'
        elif us.check_if_user_existed(username, email):
            return '4'
        else:
            result = us.register_new_user(username, email, password)
            if result == False:
                return '5'
            else:
                return '0'


@app.route('/logout', methods=['POST'])
def logout():
    try:
        session.pop('email', None)
        return '0'
    except:
        return '1'


@app.route('/simple/customer', methods=['GET'])
def customer(keyword="%"):
    if 'email' in session:
        username = us.get_name_by_email(session['email'])
        return render_template('customer.html', email=session['email'], username=username,
                               title="Customer", active_parent="SimpleSearch", active_function="customer",
                               attributes=cs.get_schema())
    else:
        return redirect(url_for('login'))


@app.route('/simple/customer/search', methods=['POST'])
def customer_search():
    if 'email' in session:
        keyword = request.form['keyword']
        results = cs.search_customer_by_keyword(keyword)
        to_return = []
        for i in range(len(results)):
            to_return.append({
                'cID': results[i][0],
                'zipcode': results[i][1]
            })
        print(to_return)
        return jsonify(to_return)
    else:
        return None


@app.route('/simple/order', methods=['GET'])
def order():
    if 'email' in session:
        username = us.get_name_by_email(session['email'])
        return render_template('order.html', email=session['email'], username=username, title="Order", active_parent="SimpleSearch", active_function="order",attributes=os.get_schema())
    else:
        return redirect(url_for('login'))


@app.route('/simple/order/search', methods=['POST'])
def order_search():
    if 'email' in session:
        keyword = request.form['keyword']
        typee = request.form['type']
        results = None
        if typee == 'order':
            results = os.search_order_by_order_id(keyword)
        else:
            results = os.search_order_by_customer_id(keyword)
        to_return = []
        for i in range(len(results)):
            to_return.append({
                'oID': results[i][0],
                'cID': results[i][1],
                'sts': results[i][2],
                'pTime': results[i][3],
                'aTime': results[i][4],
                'dTime': results[i][5],
                'rTime': results[i][6],
                'eTime': results[i][7]
            })
        print(to_return)
        return jsonify(to_return)
    else:
        return None


@app.route('/simple/product', methods=['GET'])
def product():
    if 'email' in session:
        username = us.get_name_by_email(session['email'])
        return render_template('product.html', email=session['email'], username=username, title="Product", active_parent="SimpleSearch", active_function="product")
    else:
        return redirect(url_for('login'))


@app.route('/simple/seller', methods=['GET'])
def seller():
    if 'email' in session:
        username = us.get_name_by_email(session['email'])
        return render_template('seller.html', email=session['email'], username=username, title="Seller", active_parent="SimpleSearch", active_function="seller")
    else:
        return redirect(url_for('login'))


@app.route('/test')
def test():
    data = cs.search_customer_by_keyword('cd73')
    return jsonify(data)


if __name__ == '__main__':
    app.run()
