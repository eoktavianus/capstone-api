from flask import Flask, request
import pandas as pd

app = Flask(__name__)   

@app.route('/home')
def home():
    return 'Hellow, Good Morning'

@app.route('/hello/<your_name>')
def hello(your_name):
    return 'Hello ' + str(your_name)

@app.route('/query')
def query_example():
    key1 = 'name'
    key2 = 'age'
    name = request.args[key1]
    age = request.args.get(key2)
    return (f'Hello, {name}, you are {age} years old')

@app.route('/form', methods = ['GET', 'POST'])
def form():
    if request.method == "POST":
        key1 = 'name'
        key2 = 'age'
        name = request.form.get(key1)
        age = request.form.get(key2)

        return(f'''
                <h1>Your name is : {name}</h1>
                <h1>Your age is : {age}</h1>
                ''')

    return '''<form method= "POST">
                Name : <input type='text' name="name"><br>
                Age : <input type='text' name="age"><br>
                <input type="submit" value="Submit"><br>
            </form>'''

@app.route('/json', methods = ["POST"])
def json_ep():
    req = request.get_json(force=True)
    name = req['name']
    age = req['age']
    address = req['address']

    return (f'''
            Hello {name}, your age is {age} and your address is {address}
            ''')

# mendapatkan keseluruhan data  dari file dengan bentuk Json
@app.route('/data/get/<data_name>', methods=["GET"])
def get_data(data_name):
    data = pd.read_csv('data/' + str(data_name))
    return data.to_json()

# mendapatkan data dari file dalam bentuk Json dengan filter nilai <value. dari kolom <column>
@app.route('/data/get/equal/<data_name>/<column>/<value>', methods=["GET"])
def get_databyFilter(data_name, column, value):
    data = pd.read_csv('data/' + str(data_name))
    mask = data[column] == value
    # mask = data[column].str.contains(value)
    data = data[mask]
    return (data.to_json())

# Test dynamics fetching data books_c.csv sesuai kolom dan value dari client melalui form
@app.route('/data/get/equal/form1', methods = ['GET', 'POST'])
def form1():    
    if request.method == "POST":
        data = pd.read_csv('data/books_c.csv')
        key1 = 'column'
        key2 = 'value'
        column = request.form.get(key1)
        value = request.form.get(key2)
        
        mask = data[column] == value
        data = data[mask]
        
        return(data.to_json())
        # return(f'''column {column} dan value {value}''')

    return '''<form method= "POST">    
                Search Key : <input type='text' name="column"><br>
                Search Value : <input type='text' name="value"><br> 
                <input type="submit" value="Submit"><br>
            </form>'''

# Test dynamics fetching data books_c.csv sesuai kolom dan value dari client melalui form
@app.route('/data/get/equal/form', methods = ['GET', 'POST'])
def form_equal():    
    if request.method == "POST":
        data = pd.read_csv('data/books_c.csv')
        key1 = 'rating1'
        key2 = 'rating2'
        startrating = request.form.get(key1)
        endrating = request.form.get(key2)
        
        mask = (data['average_rating'] >= float(startrating)) & (data['average_rating'] <= float(endrating))
        data = data[mask]
        
        return(data.to_json())
        # return(f'''column {column} dan value {value}''')

    return '''<form method= "POST">    
                average_rating :  <input type='text' name="rating1">
                - <input type='text' name="rating2"><br> 
                <input type="submit" value="Submit"><br>
            </form>'''


if __name__ == '__main__':
    app.run(debug=True, port=5001)