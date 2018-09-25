#author: Kanchi Chitaliya kach6618@colorado.edu
#date:10/31/2017
#version: 3.6.2
#file_name:file1.py
#purpose: introduction to Flask

from flask import Flask,render_template,Markup,request
import os
import logging
import sqlite3
app=Flask(__name__)

@app.route('/index')
def index():
    bodyText=Markup('<b>Select your option</b><br><a href="/planets">Planets Database</a><br><a href="/form">Form</a>')
    try:
        return render_template("index.html",bodyText=bodyText)
    except:
        logging.error("File not present in templates")
        quit()

@app.route("/planets")
def planets():
    try:
        os.path.isfile("planets.db")
        db=sqlite3.connect("planets.db")
        db.row_factory=sqlite3.Row
        query="select planets,mass,distance_from_sun,diameter,no_of_moons from planets"
        cursor=db.cursor()
        cursor.execute(query)
        rows=cursor.fetchall()
        var=""
        for i in rows:
            var +=Markup("<tr><td>"+str(i[0])+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td><td>"+str(i[4])+"</td></tr>")
        try:
            return render_template("tables.html",bodyText=var)
        except:
            logging.error("File not present in templates")
            quit()

    except:
        logging.error("Database not present in the directory")
        quit()

@app.route("/form",methods=['GET','POST'])
def form():
    
    if request.method=="GET":
        try:
            return render_template("form.html")
        except:
            logging.error("File not present in templates")
            quit()
    elif request.method=="POST":
        try:
            os.path.isfile("planets.db")
            Planet_Name=request.form["Planet_Name"]
    
            db=sqlite3.connect("planets.db")
            db.row_factory=sqlite3.Row
            query="select planets,mass,distance_from_sun,diameter,no_of_moons from planets where planets=?"
            t=(Planet_Name,)
            cursor=db.cursor()
            cursor.execute(query,t)
            rows=cursor.fetchall()
            var=""
            for i in rows:
                var +=Markup("<tr><td>"+str(i[0])+"</td><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td><td>"+str(i[4])+"</td></tr>")
                try:
                    return render_template("tables.html",bodyText=var)
                except:
                    logging.error("File not present in templates")
                    quit()
        except:
            logging.error("Database not present in the directory")
            quit()
            
if __name__=='__main__':
    app.debug=True
    logging.basicConfig(format="%(asctime)s [%(levelname)s] %(message)s", filename="loggers.log",level=logging.DEBUG)
    app.run(host='0.0.0.0',port=80)
