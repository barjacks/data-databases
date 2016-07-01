
from flask import Flask, jsonify, request
import pg8000

app = Flask(__name__)
conn = pg8000.connect(user='barneyjs', database="mondial")

#Creating a function to change values into ints, skipping the Nones
def int_(x):
    if x is None:
        return None
    else:
        return int(x)

#Creating a function to change values into strs, skipping the Nones
def str_(x):
    if x is None:
        return None
    else:
        return str(x)

@app.route('/lakes')
def get_lakes():
    cursor = conn.cursor()
    #ORDER BY NAME, ORDER BY AREA, ORDER BY ELEVATION
    #order_by = 'ORDER BY name'
    #print(order_by)

    #Getting the variable for the sorting
    #print(get_variable)
    get_variable = request.args.get('sort', '')
    print(get_variable)
    #print(get_variable) for debugging
    if get_variable == 'name':
        order_by = 'ORDER BY name'
        print(order_by)
        #print(order_by) for debugging
    elif get_variable == 'elevation':
        order_by = 'ORDER BY elevation DESC'
    elif get_variable == 'area':
        order_by = 'ORDER BY area DESC'
    else:
        order_by = 'ORDER BY name'
        print(order_by, 'else')

    #Getting the variable for the type filtering
    #SQL statement = 'SELECT name, elevation, area, type FROM lake ' + order_by + ' WHERE type=salt'
    #print(get_variable)
    gt_typ = request.args.get('type', '')
    if gt_typ == 'salt':
        get_type = 'salt'
        cursor.execute('SELECT name, elevation, area, type FROM lake WHERE type=%s ' + order_by, [get_type])
    elif gt_typ == 'dam':
        get_type = 'dam'
        cursor.execute('SELECT name, elevation, area, type FROM lake WHERE type=%s ' + order_by, [get_type])
    elif gt_typ == 'caldera':
        get_type = 'caldera'
        cursor.execute('SELECT name, elevation, area, type FROM lake WHERE type=%s ' + order_by, [get_type])
    else:
        cursor.execute('SELECT name, elevation, area, type FROM lake ' + order_by)

    #cursor.execute('SELECT name, elevation, area, type FROM lake WHERE type=%s ' + order_by, [get_type])
    print(cursor.execute)

    output = []
    for item in cursor.fetchall():
        output.append({'name': item[0], 'elevation': int_(item[1]), 'area': int_(item[2]), 'type': str_(item[3])})
    return jsonify(output)

app.run()
#http://localhost:5000/lakes
#http://localhost:5000/lakes
#http://localhost:5000/lakes


# In[ ]:
