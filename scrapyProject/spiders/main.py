#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 13:58:41 2021

@author: justinlien
"""


import pandas as pd 
from data_process import Data_process as dp
from flask import Flask, request, url_for, redirect, render_template


db = dp.db_conn()

mycursor = db.cursor()


# dynamic select database and create a table

table_name=input("Name first table:")
mycursor.execute(f"CREATE TABLE {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, question VARCHAR(255), view VARCHAR(255), answer VARCHAR(255), vote VARCHAR(255))")
db.commit()


lan_table=input("Name second table:")
mycursor.execute(f"CREATE TABLE {lan_table} (id INT AUTO_INCREMENT PRIMARY KEY,l1 VARCHAR(45) ,l2 VARCHAR(45) ,l3 VARCHAR(45) ,l4 VARCHAR(45) ,l5 VARCHAR(45) ,l6 VARCHAR(45) ,l7 VARCHAR(45),l8 VARCHAR(45),amount VARCHAR(45))")
db.commit()

statistic_table=input("Name third table:")
mycursor.execute(f"CREATE TABLE {statistic_table} (name VARCHAR(225) PRIMARY KEY NOT NULL,amount VARCHAR(45))")
db.commit()

data=dp.import_data("abc.jl")
while(data.count({'languages': []})):
    data.remove({'languages': []})

#splite data into 5 column
list1=[]
list2=[]
list3=[]
list4=[]
list5=[]
for i in range(0,49):
    list1.append(data[i].get('question'))
    
for i in range(50,99):
    list2.append(data[i].get('views'))
for i in range(100,149):
    list3.append(data[i].get('answers'))
for i in range(150,199):
    list4.append(data[i].get('votes'))
for i in range(200,249):
    list5.append(data[i].get('languages'))


#insert data into first table
x=[] 
for i in range(0,49):
    x.append(i+1)
    x.append(list1[i])
    x.append(list2[i])
    x.append(list3[i])
    x.append(list4[i])

    sql=f"INSERT INTO {table_name}(id,question,view,answer,vote) VALUES(%s,%s,%s,%s,%s)"
    
    mycursor.execute(sql,tuple(x))
    db.commit()
    x=[]
    

java=0
cplus=0
javascript=0
git=0
c=0
python=0
csharp=0
linux=0
http=0


#create second table
for i in range(0,49):

    sql=f"INSERT INTO {lan_table}(l1,l2,l3,l4,l5,l6,l7,l8,amount) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    x=[]
    x+=list5[i]
    #prepare data for third table
    for m in range(0,len(list5[i])):
        s="".join(str(list5[i][m]))
        if(list5[i][m]=="java"):
            java+=1
        if(list5[i][m]=="c#"):
            csharp+=1
        if(list5[i][m]=="c++"):
            cplus+=1
        if(list5[i][m]=="linux"):
            linux+=1
        if(list5[i][m]=="http"):
            http+=1
        if(list5[i][m]=="python"):
            python+=1
        if(list5[i][m]=="javascript"):
            javascript+=1
        if(s[:3]=="git"):
            git+=1
        if(list5[i][m]=="c"):
            c+=1
    #if data didn't have eight tags,append null
    r=[]
    for o in range(len(x),8):
        r.append("null")
    x+=r
    x.append(len(list5[i]))
    print(x)
    mycursor.execute(sql,tuple(x))
    db.commit()

#create third table
x=[java,
cplus,
javascript,
git,
c,
python,
csharp,
linux,
http]

y=["java",
"c++",
"javascript",
"git",
"c",
"python",
"csharp",
"linux",
"http"]

z=[]

for i in range(0,len(x)):
    z=[]
    z.append(y[i])
    z.append(x[i])
    sql=f"INSERT INTO {statistic_table}(name,amount) VALUES(%s,%s)"
    mycursor.execute(sql,tuple(z))
    db.commit()



#create dataframe and server
df = pd.DataFrame(list(zip(list1, list2, list3, list4, list5)), columns=['Question','View','Answer','Vote','Language'] ) 

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=("POST", "GET"))
def index():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('home.html')
@app.route('/result/', methods=("POST", "GET"))
def result():
    return render_template('index.html', tables=[df.to_html(classes='data')], titles=df.columns.values)

@app.route('/member', methods=['GET', 'POST'])
def member():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('members.html')
@app.route('/abstract', methods=['GET', 'POST'])
def abstract():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('abstract.html')
@app.route('/database', methods=['GET', 'POST'])
def database():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('database.html')      
@app.route('/conclusion', methods=['GET', 'POST'])
def conclusion():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('conclusion.html')
if __name__ == '__main__':
  app.run(debug=False)
