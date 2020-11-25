"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, request,render_template
import pymysql.cursors

def execute(sql, isSelect = True):
    conn = pymysql.connect(host='127.0.0.1',
                           port=3306,
                           user='bersim-8',
                           password='SecretPassword',
                           db ='D0018E',
                           charset='utf8mb4',
                           cursorclass=pymysql.cursors.DictCursor)
    result = None
    try:
        with conn.cursor() as cursor:
            if isSelect:
                cursor.execute(sql)
                result = cursor.fetchall()
            else:
                cursor.execute(sql)
                result = conn.insert_id()
                conn.commit()
    finally:
        conn.close()
    return result


def parse_product_data(data, keys):

    data_content = [data['Insert']]

    for i in range(1, len(keys)-1):
        print(data[keys[i]])
        if data[keys[i]] != "":
            data_content.append(data[keys[i]])
        else:
            continue

    print("hm")
    new_data = (keys, data_content)
    print(new_data)
    return new_data

app = Flask(__name__)

@app.route("/")
def hello():
    sql = "Select PName, PPrice from D0018E.Product"
    data = execute(sql)
    return render_template("test.html", data = data)

@app.route('/', methods=['POST'])
def my_form_post():

    req = request.form
    print(req)
    keys = ['PID', 'PName', 'PPrice', 'PStock', 'PColor', 'PDescript', 'PRating']
    
    if 'Insert' in req:
        
        data = parse_product_data(req, keys)
        print(data)
        sql = ("INSERT INTO D0018E.Product(PID, PName, PPrice, PStock, PColor, PDescript, PRating) VALUES ({})".format(data))
        res = execute(sql, False)
            
    elif 'Update' in req:
        
        data = parse_product_data(req, keys)
        print(data)
        update = tuple(update.split(", "))
        sql = ("UPDATE D0018E.Product SET PPrice = " + update[1] + " WHERE PID = " + update[0]) 
        res = execute(sql, False)
        
    sql = "Select PName, PPrice from D0018E.Product"
    data = execute(sql)
    return render_template("test.html", data = data)

@app.route("/Kenobi")
def kenobi():
    return render_template("bold_one.html")

@app.route("/data")
def data():
    sql = "Select * from D0018E.test"
    data = execute(sql)
    print(data)
    return render_template("table.html", data = data)

@app.route("/readTable")
def readTable():
    sql = "SELECT CID, CFName FROM D0018E.Customer WHERE CID = '11223344';"
    table = execute(sql)
    print(table)
    return render_template("readTable.html", table = table)

@app.route("/admin")
def admin():
    sql = "SELECT AID, AFName, ALName, AMail FROM D0018E.Administrator;"
    adminTable = execute(sql)
    print(adminTable)
    return render_template("Admin.html", adminTable = adminTable)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
