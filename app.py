from flask import Flask, request, render_template, session, redirect, url_for, jsonify
from service import product_service as ps, seller_service as ss, customer_service as cs, user_service as us, \
    order_service as os
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta

app = Flask(__name__)
app.secret_key = b'I9e0n6_2w2q'


@app.route('/', methods=['GET'])
def index():
    if 'email' in session:
        username = us.get_name_by_email(session['email'])
        return render_template('starter.html', email=session['email'], username=username, title="Dashboard",
                               active_parent="Dashboard", active_function="dashboard")
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
        return render_template('simple/customer.html', email=session['email'], username=username,
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
        return render_template('simple/order.html', email=session['email'], username=username, title="Order",
                               active_parent="SimpleSearch", active_function="order", attributes=os.get_schema())
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
        return render_template('simple/product.html', email=session['email'], username=username, title="Product",
                               active_parent="SimpleSearch", active_function="product", attributes=ps.get_schema())
    else:
        return redirect(url_for('login'))


@app.route('/simple/product/search', methods=['POST'])
def product_search():
    if 'email' in session:
        keyword = request.form['keyword']
        results = ps.search_product_by_id(keyword)
        to_return = []
        for i in range(len(results)):
            to_return.append({
                'pID': results[i][0],
                'category': results[i][1],
                'name_length': results[i][2],
                'weight': results[i][3],
                'length': results[i][4],
                'height': results[i][5],
                'width': results[i][6]
            })
        print(to_return)
        return jsonify(to_return)
    else:
        return None


@app.route('/simple/seller', methods=['GET'])
def seller():
    if 'email' in session:
        username = us.get_name_by_email(session['email'])
        return render_template('simple/seller.html', email=session['email'], username=username, title="Seller",
                               active_parent="SimpleSearch", active_function="seller", attributes=ss.get_schema())
    else:
        return redirect(url_for('login'))


@app.route('/simple/seller/search', methods=['POST'])
def seller_search():
    if 'email' in session:
        keyword = request.form['keyword']
        results = ss.search_seller_by_id(keyword)
        to_return = []
        for i in range(len(results)):
            to_return.append({
                'sID': results[i][0],
                'zipcode': results[i][1]
            })
        print(to_return)
        return jsonify(to_return)
    else:
        return None


@app.route('/advanced/product')
def advanced_product():
    if 'email' in session:
        username = us.get_name_by_email(session['email'])
        return render_template('advanced/product.html', email=session['email'], username=username, title="SaleProduct",
                               active_parent="AdvancedAnalysis", active_function="SaleProduct")
    else:
        return redirect(url_for('login'))


@app.route('/advanced/product/get_data', methods=['POST'])
def draw_line_product():
    if 'email' in session:
        product_id = request.form['product_id']
        end_date = request.form['end_date']
        start_date = request.form['start_date']
        results = ps.draw_line_product(start_date, end_date, product_id)
        month_slot = get_months(start_date, end_date)

        for r in results:
            month_slot[r[1]] = r[0]

        to_return = {
            'time': [],
            'value': []
        }
        for m in month_slot.items():
            to_return['time'].append(m[0])
            to_return['value'].append(m[1])

        return jsonify(to_return)
    else:
        return None


@app.route('/advanced/location')
def advanced_location():
    if 'email' in session:
        username = us.get_name_by_email(session['email'])
        return render_template('advanced/location.html', email=session['email'], username=username, title="SaleLocation",
                               active_parent="AdvancedAnalysis", active_function="SaleLocation")
    else:
        return redirect(url_for('login'))


@app.route('/advanced/category')
def advanced_category():
    if 'email' in session:
        username = us.get_name_by_email(session['email'])
        return render_template('advanced/category.html', email=session['email'], username=username, title="SaleCategory",
                               active_parent="AdvancedAnalysis", active_function="SaleCategory")
    else:
        return redirect(url_for('login'))


@app.route('/advanced/customer')
def advanced_customer():
    if 'email' in session:
        username = us.get_name_by_email(session['email'])
        return render_template('advanced/customer.html', email=session['email'], username=username, title="UserTrend",
                               active_parent="AdvancedAnalysis", active_function="UserTrend")
    else:
        return redirect(url_for('login'))


@app.route('/advanced/delivery')
def advanced_delivery():
    if 'email' in session:
        username = us.get_name_by_email(session['email'])
        return render_template('advanced/delivery.html', email=session['email'], username=username, title="DeliveryTrend",
                               active_parent="AdvancedAnalysis", active_function="DeliveryTrend")
    else:
        return redirect(url_for('login'))


@app.route('/advanced/satisfactory')
def advanced_satisfactory():
    if 'email' in session:
        username = us.get_name_by_email(session['email'])
        return render_template('advanced/satisfactory.html', email=session['email'], username=username, title="SatisfactoryTrend",
                               active_parent="AdvancedAnalysis", active_function="SatisfactoryTrend")
    else:
        return redirect(url_for('login'))


@app.route('/test', methods=['GET'])
def test():
    product_id = 'aca2eb7d00ea1a7b8ebd4e68314663af'
    end_date = '2018-05'
    start_date = '2017-02'
    results = ps.draw_line_product(start_date, end_date, product_id)

    month_slot = get_months(start_date, end_date)

    for r in results:
        month_slot[r[1]] = r[0]

    to_return = {
        'time': [],
        'value': []
    }
    for m in month_slot.items():
        to_return['time'].append(m[0])
        to_return['value'].append(m[1])

    return jsonify(to_return)


if __name__ == '__main__':

    app.run()


def get_months(start, end):
    start_dt = datetime.strptime(start, '%Y-%m').date()
    end_dt = datetime.strptime(end, '%Y-%m').date()
    month_slot = {}

    while start_dt <= end_dt:
        month_slot[start_dt.strftime('%Y-%m')] = 0
        start_dt += relativedelta(months=1)
    return month_slot
