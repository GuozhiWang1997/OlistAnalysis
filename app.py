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

#3-1
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

#3-5
@app.route('/advanced/delivery/get_data', methods = ['POST'])
def draw_delivery_histogram():
    if 'email' in session:
        state1 = request.form['state1']
        city1 = request.form['city1']
        state2 = request.form['state2']
        city2 = request.form['city2']
        results = os.draw_delivery_histogram(state1,city1, state2, city2)
        month_slot = get_months(results[0][2], results[len(results) - 1][2])
        month_slot1 = get_months(results[0][2], results[len(results) - 1][2])

        to_return = {
            'time': [],
            'prep_time': [],
            'deli_time': []
        }
        for r in results:
            month_slot[r[2]] = r[0]
            month_slot1[r[2]] = r[1]

        for m in month_slot.items():
            to_return['time'].append(m[0])
            to_return['prep_time'].append(m[1])
            to_return['deli_time'].append(month_slot1[m[0]])

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

#3-3
@app.route('/advanced/category/get_data', methods=['POST'])
def draw_stacked_map():
    if 'email' in session:
        category_list = request.form['category_list']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        list1 = []
        category_str = ""
        for i in category_list:
            list1.append("\'" + i + "\'")
            category_str = ','.join(list1)

        results = ps.draw_stacked_map(category_str, start_date, end_date)
        month_slot = get_months(start_date, end_date)

        for category in category_list:
            month_slot1 = {}
            for i in results:
                if i[1] == category:
                    month_slot1[i[2]] = i[0]

            for i in month_slot.keys():
                if i not in month_slot1.keys():
                    month_slot1[i] = 0

            to_return = {
                'time': [],
                'cnt': []
            }
            for i in month_slot1.items():
                to_return['time'].append(i[0])
                to_return['cnt'].append(i[1])
        return jsonify(to_return)
    else:
        return None


@app.route('/advanced/customer')
def advanced_customer():
    if 'email' in session:
        username = us.get_name_by_email(session['email'])
        return render_template('advanced/customer.html', email=session['email'], username=username, title="UserTrend",
                               active_parent="AdvancedAnalysis", active_function="UserTrend")
    else:
        return redirect(url_for('login'))

#3-4
@app.route('/advanced/customer/get_data', methods = ['POST'])
def draw_customer_histogram():
    if 'email' in session:
        end_date = request.form['end_date']
        start_date = request.form['start_date']
        results = cs.draw_customer_histogram(start_date, end_date)
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

#3-6
@app.route('/advanced/satisfactory/get_data', methods=['POST'])
def draw_satisfactory_histogram():
    if 'email' in session:
        product_id = request.form['product_id']
        results = ps.draw_satisfactory_histogram(product_id)
        print(results)
        month_slot = get_months(results[0][1], results[len(results) - 1][1])
        print(month_slot)
        to_return = {
            'time': [],
            'value': [],
        }
        for r in results:
            month_slot[r[1]] = r[0]
        print(month_slot)

        for m in month_slot.items():
            to_return['time'].append(m[0])
            to_return['value'].append(m[1])

        return jsonify(to_return)

    else:
        return None


@app.route('/test', methods=['GET'])
def test():
    category_list = ["esporte_lazer", "cama_mesa_banho"]
    list1 = []
    category_str = ""
    for i in category_list:
        list1.append("\'" + i + "\'")
        category_str = ','.join(list1)
    end_date = "2018-10"
    start_date = "2016-10"
    results = ps.draw_stacked_map(category_str, start_date, end_date)
    month_slot = get_months(start_date, end_date)
    for category in category_list:
        month_slot1 = {}
        for i in results:
            if i[1] == category:
                month_slot1[i[2]] = i[0]

        for i in month_slot.keys():
            if i not in month_slot1.keys():
                month_slot1[i] = 0

        to_return = {
            'time': [],
            'cnt': []
        }
        for i in month_slot1.items():
            to_return['time'].append(i[0])
            to_return['cnt'].append(i[1])



    # print(results)
    # product_id = 'b6f3b8136ba8302906df7e11ff908751'
    # results = ps.draw_satisfactory_histogram(product_id)
    # print(results)
    # month_slot = get_months(results[0][1], results[len(results) - 1][1])
    # print(month_slot)
    # to_return = {
    #     'time': [],
    #     'value': [],
    # }
    # for r in results:
    #     month_slot[r[1]] = r[0]
    # print(month_slot)
    #
    # for m in month_slot.items():
    #     to_return['time'].append(m[0])
    #     to_return['value'].append(m[1])
    #
    # return jsonify(to_return)


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
