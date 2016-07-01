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

@app.route("/lakes")
def get_lakes():
    cursor = conn.cursor()
    sort_by = request.args.get('sort_by', 'name')
    ty_gt = request.args.get('type_gt', 'salt')
    if sort_by == 'name':
        sort_string = 'ORDER BY name'
    else:
        sort_string = 'ORDER BY ' + sort_by + ' DESC'
    cursor.execute('SELECT name, elevation, area, type FROM lake WHERE type=%s' + sort_string, [ty_gt])
    output = []
    for item in cursor.fetchall():
        output.append({'name': item[0], 'elevation': int_(item[1]), 'area': int_(item[2]), 'type': str_(item[3])})
    return jsonify(output)

app.run()
#http://localhost:5000/lakes
