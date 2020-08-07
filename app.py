from flask import Flask, request
import requests
import pandas as pd
import sqlite3
import os
import json

app = Flask(__name__)   

@app.route('/')
def home():
    return 'Hellow, Welcome to my capstone project Have a Great Day'

@app.route('/home')
def home2():
    return 'Hellow, Good Morning'

@app.route('/hello/<your_name>', methods={"GET"})
def hello(your_name):
    return 'Hello ' + str(your_name)

@app.route('/query', methods={"GET"})
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

@app.route('/data/getbyfileext/<data_name>', methods=["GET"])
def get_databyFileExt(data_name):
    fname, fext = os.path.splitext(data_name)
    if fext == '.db':
        conn = sqlite3.connect('data/' + str(data_name))
        dt = pd.read_sql_query('''SELECT * FROM customers  LIMIT 5''', conn)
    elif fext == '.csv':
        dt = pd.read_csv('data/' + str(data_name))
    else:
        dt = pd.DataFrame({"Message" : ["File Not Recognize"]})

    return dt.to_json()

'''
 question 1 : Top 5 Books berdasarkan Ratings count tertinggi
 question 2 : Top 5 Books berdasarkan halaman terbanyak
'''
@app.route('/question/form/', methods = ["GET", "POST"])
def get_answer_form():
    if request.method == "POST":
        key1 = 'quest'
        questopt = request.form.get(key1)
        books = pd.read_csv('data/books_c.csv')
        if questopt == '1':
            data = books.sort_values(by=['ratings_count'], ascending=False).head()
        else:
            data = books.sort_values(by=['# num_pages'], ascending=False).head()
        return data.to_json()
    
    
    return '''<form method= "POST">    
                Ask Me :
                <select name='quest'>
                    <option value="1">Top 5 Books with HIghest Ratings count</option>
                    <option value="2">Top 5 Books dengan halaman terbanyak</option>
                </select><br>
                <input type="submit" value="Submit"><br>
            </form>'''

# sama dengan pertanyaan sebelumnya hanya fetch data via query
@app.route('/question/query', methods = ["GET"])
def get_answer_query():
    key1 = 'questopt'
    questopt = request.args.get(key1)
    books = pd.read_csv('data/books_c.csv')
    if questopt == '1':
        data = books.sort_values(by=['ratings_count'], ascending=False).head()
    else:
        data = books.sort_values(by=['# num_pages'], ascending=False).head()
    return data.to_json()

# Static Endpoint 1 : Get Data Authors
@app.route('/get/author', methods=["GET"])
def get_authors():
    books = pd.read_csv('data/books_c.csv')
    books.authors = books.authors.astype('category')
    data = pd.DataFrame(books.authors.unique())
    return data.to_json()

# Static Endpoint 2 : Get Total and List Book English Version
@app.route('/get/englishversion', methods=["GET"])
def get_englishversion():
    books = pd.read_csv('data/books_c.csv')
    data = books[books.language_code == 'eng']
    total = data.bookID.count()
    dt = pd.DataFrame({"Total English Version" : [total],
                        "ListBook" : [data]
                    })
    return dt.to_json()

# EDA Group BY DataFrame
@app.route('/eda/groupby', methods={"GET"}) 
def eda_groupby():
    books2 = pd.read_csv('data/books_c.csv')
    data1 = books2[['authors','# num_pages']]
    data = data1.groupby(['authors']).mean().sort_values(by='# num_pages', ascending=False).reset_index().head()
    return data.to_json()

# EDA Categorical n Freq with sql
@app.route('/eda/catfreq/sql/', methods=["GET"])
def eda_catfreq_sql():
    conn = sqlite3.connect('data/chinook.db')
    dtGenre = pd.read_sql_query('''
                        SELECT g.Name Genre, c.Country,
                            CASE CAST(strftime('%w', i.InvoiceDate) AS integer)
                              when 0 then 'Sunday'
                              when 1 then 'Monday'
                              when 2 then 'Tuesday'
                              when 3 then 'Wednesday'
                              when 4 then 'Thursday'
                              when 5 then 'Friday'
                              else 'Saturday'
                            END as InvoiceWD,
                            SUM(ii.Quantity) TotalQty
                        FROM invoices i
                        LEFT JOIN invoice_items ii ON i.invoiceId = ii.invoiceId
                        LEFT JOIN customers c ON c.CustomerId = i.CustomerId
                        LEFT JOIN Tracks t ON t.TrackId = ii.TrackId
                        LEFT JOIN Genres g ON g.GenreId = t.GenreId
                        LEFT JOIN Albums al ON al.AlbumId = t.AlbumId
                        LEFT JOIN Artists ar ON ar.ArtistId = al.ArtistId
                        WHERE c.Country = 'Germany' AND CAST(strftime('%w', i.InvoiceDate) AS integer) = 1
                        GROUP BY g.Name, c.Country,
                            CASE CAST(strftime('%w', i.InvoiceDate) AS integer)
                              when 0 then 'Sunday'
                              when 1 then 'Monday'
                              when 2 then 'Tuesday'
                              when 3 then 'Wednesday'
                              when 4 then 'Thursday'
                              when 5 then 'Friday'
                              else 'Saturday'
                            END 
                        ORDER BY TotalQty DESC
                        ''', conn)
    return dtGenre.to_json()

def get_dtDate():
    conn = sqlite3.connect('data/chinook.db')
    dtDate = pd.read_sql_query('''
                        SELECT i.*, c.Country,
                            ii.TrackId, ii.UnitPrice, ii.Quantity, ii.UnitPrice * ii.Quantity as TotalPriceDtl,
                            t.Name TrackName, t.Composer, g.Name Genre, ar.Name artis
                        FROM invoices i
                        LEFT JOIN invoice_items ii ON i.invoiceId = ii.invoiceId
                        LEFT JOIN customers c ON c.CustomerId = i.CustomerId
                        LEFT JOIN Tracks t ON t.TrackId = ii.TrackId
                        LEFT JOIN Genres g ON g.GenreId = t.GenreId
                        LEFT JOIN Albums al ON al.AlbumId = t.AlbumId
                        LEFT JOIN Artists ar ON ar.ArtistId = al.ArtistId
                        ''', conn,
                        parse_dates='InvoiceDate')
    dtDate['InvoiceWD'] = dtDate['InvoiceDate'].dt.day_name()
    return dtDate

# EDA Categorical n Freq with pandas
@app.route('/eda/catfreq', methods=["GET"])
def eda_catfreq():
#     url = 'https://capsapi.herokuapp.com/data/join/date'
#     h = requests.get(url)
#     dtDate = pd.DataFrame(h.json())
    dtDate = get_dtDate()
    dtx = dtDate[(dtDate.Country == 'Germany') & (dtDate.InvoiceWD == 'Monday')].\
            groupby(['Country', 'InvoiceWD', 'Genre']).sum().\
            sort_values(by='Quantity', ascending=False).reset_index()
    dtx = dtx[['Country', 'InvoiceWD', 'Genre', 'Quantity']].head()
    return dtDate.to_json()


# Fetch Data Table from Chinook.db
@app.route('/get/data/table/<table_name>', methods={"GET"})
def get_chinook_table(table_name):
    conn = sqlite3.connect('data/chinook.db')
    sSQL = 'SELECT * FROM ' + str(table_name)
    data = pd.read_sql_query(sSQL, conn)
    return data.to_json()

# EDA datetime + Joining > 4 Table
@app.route('/data/join/date')
def get_data_multitable_date():
    conn = sqlite3.connect('data/chinook.db')
    data = pd.read_sql_query('''
                        SELECT i.*, c.Country,
                            ii.TrackId, ii.UnitPrice, ii.Quantity, ii.UnitPrice * ii.Quantity as TotalPriceDtl,
                            t.Name TrackName, t.Composer, g.Name Genre, ar.Name artis
                        FROM invoices i
                        LEFT JOIN invoice_items ii ON i.invoiceId = ii.invoiceId
                        LEFT JOIN customers c ON c.CustomerId = i.CustomerId
                        LEFT JOIN Tracks t ON t.TrackId = ii.TrackId
                        LEFT JOIN Genres g ON g.GenreId = t.GenreId
                        LEFT JOIN Albums al ON al.AlbumId = t.AlbumId
                        LEFT JOIN Artists ar ON ar.ArtistId = al.ArtistId
                        ''', conn,
                          parse_dates='InvoiceDate')
    data['InvoiceWD'] = data['InvoiceDate'].dt.day_name()
    return data.to_json()

# reshapping visualization stack
@app.route('/resviz/stack', methods=["GET"])
def resviz_stack():
    pfile = 'data/dtx2'
    dtDate = get_dtDate()
    dtx2 = dtDate[(dtDate.Country == 'Germany') & (dtDate.InvoiceWD == 'Monday')].\
        pivot_table(index=['Country', 'InvoiceWD'],
                    columns='Genre',
                   values='Quantity',
                   aggfunc='sum')
    dtx2 = dtx2.unstack().stack(level=0)
    # dtx2.to_pickle(pfile)
    # dt = pd.DataFrame([{"filepath" : pfile}])
    dtx2 = dtx2.reset_index()
    return dt.to_json()

if __name__ == '__main__':
    app.run(debug=True, port=5000)