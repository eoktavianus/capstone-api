# p4da-capstone-api
This is Algoritma's Python for Data Analysis Capstone Project. This project aims to create a simple API to fetch data from Heroku Server. 

As a Data Scientist, we demand data to be accessible. And as a data owner, we are careful with our data. As the answer, data owner create an API for anyone who are granted access to the data to collect them. In this capstone project, we will create Flask Application as an API and deploy it to Heroku Web Hosting. 

We provide a brief guideline to create the API and how to Deploy in `Capstone Guideline.ipynb` using Bahasa Indonesia. 

You can check the rubrics on rubrics folder
___
## Dependencies : 
- Pandas    (pip install pandas)
- Flask     (pip install flask)
- Gunicorn  (pip install gunicorn)
___
## Goal 
- Create Flask API App
- Deploy to Heroku
- Build API Documentation of how your API works
- Implements the data analysis and wrangling behind the works

___
We have deployed a simple example on : https://capsapi.herokuapp.com
Here's the list of its endpoints: 
```
1. /
Base Endpoint, returning welcoming string value. 

2. /data/get/<data_name> , method = GET
Return full data <data_name> in JSON format. Currently available data are:
    - books_c.csv
    - pulsar_stars.csv 
    
3. /data/get/equal/<data_name>/<column>/<value> , method = GET
Return all <data_name> where the value of column <column> is equal to <value>

4. /home
Retunn static value, welcome greetings string value.

5. /hello/<your_name>, method = GET
Return greetings to <your_name> string value

6. /query?name=<name>&age=<age>,  method = GET
Return value string Hello, <name>, you are <age> years old

7. /form, method = GET, POST
GET --> Return Blank Form to fill Name, Age and Button Submit
SUBMIT --> Return value 
        Your name is : <name>
        Your age is : <age>

8. /json, method = POST
Return value from json file, Hello <name>, your age is <age> and your address is <address>

9. /data/get/<data_name>,  method = GET
Return all <data_name>

10. /data/get/equal/form, method = GET, POST
Return all data books_c.csv where average_rating between start and end input value 

11. /data/getbyfileext/<data_name>,  method = GET
Return all <data_name> from file .csv or return data customers in chinook.db
```

**no 12 - 15 for quest endpoint (2 statics and 1 dynamics)**
```
12. /question/form/, method = GET, POST
Return all data books_c.csv according to selected question in combobox, where the options questions are:
 question 1 : Top 5 Books berdasarkan Ratings count tertinggi
 question 2 : Top 5 Books berdasarkan halaman terbanyak

13. /question/query, method = GET
curl: https://capsapi.herokuapp.com/question/query?questopt=1
Return all data books_c.csv according to "questopt" value given, where the value are:
 1 : Top 5 Books berdasarkan Ratings count tertinggi
 2 : Top 5 Books berdasarkan halaman terbanyak

14. /get/author, method = GET
Return all Authors from books_c.csv

15. /get/englishversion, method = GET
Return Total and List Book English Version from books_c.csv
```

**Project Capstone EDA groupby DataFrame**
```
16. /eda/groupby', method = GET
Return data Authors from books_c.csv with the highest # num_pages
```

**Project Capstone Take data from joining minimum of 4 table**
```
17. /eda/catfreq/sql/
Return data Genre, Country from books_c.csv with the highest sell qty in Monday using sql
```

**Project Capstone Categorical operation & Frequencies analysis**
```
18. /eda/catfreq
Return data Genre, Country from books_c.csv with the highest sell qty in Monday using pandas dataframe technique

19. /get/data/table/<table_name>
Return all data from <table_name> in chinook.db
```

**Project Capstone Datetime operation + Joining Table**
```
20. /data/join/date
Return data invoices and detail items from multiple table in chinook.db

```

If you want to try it, you can access (copy-paste it) : 
- https://capsapi.herokuapp.com/home
- https://capsapi.herokuapp.com/data/get/books_c.csv
- https://capsapi.herokuapp.com/data/get/pulsar_stars.csv
- https://capsapi.herokuapp.com//data/getbyfileext/books_c.csv
- https://capsapi.herokuapp.com//data/getbyfileext/chinook.db
- https://capsapi.herokuapp.com/data/get/equal/books_c.csv/isbn/0439785960
- https://capsapi.herokuapp.com/question/form
- https://capsapi.herokuapp.com/question/query?questopt=1
- and so on, just follow the endpoint's pattern