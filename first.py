from flask import Flask, redirect, url_for, render_template, request
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse.linalg import svds
from sklearn.preprocessing import LabelEncoder
from tqdm import tqdm
from scipy.sparse import coo_matrix, csr_matrix
from subprocess import check_output
import csv
import json


app = Flask(__name__)

csvFile1 = open("sym1.csv", "r")
fieldNames1 = ("syd", "symptom")

csvFile2 = open("sym2.csv", "r")
fieldNames2 = ("syd", "symptom")

csvFile3 = open("sym3.csv", "r")
fieldNames3 = ("syd", "symptom")

csvFile4 = open("sym4.csv", "r")
fieldNames4 = ("syd", "symptom")

reader1 = csv.DictReader(csvFile1, fieldNames1)
rows1 = []

reader2 = csv.DictReader(csvFile2, fieldNames2)
rows2 = []

reader3 = csv.DictReader(csvFile3, fieldNames3)
rows3 = []

reader4 = csv.DictReader(csvFile4, fieldNames4)
rows4 = []

for row1 in reader1:
    rows1.append(row1["symptom"])
for row2 in reader2:
    rows2.append(row2["symptom"])
for row3 in reader3:
    rows3.append(row3["symptom"])
for row4 in reader4:
    rows4.append(row4["symptom"])









@app.route("/")
def home():
    return render_template("index.html", content="Testing")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        req = request.form 
        name = req["fullname"]
        email = req["email"]
        print(name, email)

        return redirect(url_for("symptoms"))
    return render_template("login.html")

x=0
@app.route("/symptoms", methods = ["POST", "GET"])
def symptoms():
    if request.method == "POST":
        req = request.form
        symp = req["symptom"]
        print(type(symp))
        x = int(symp)
        

        
        pass
    
    return render_template("symptoms.html", len1 = len(rows1), rows1 = rows1,
                                            len2 = len(rows2), rows2 = rows2,
                                            len3 = len(rows3), rows3 = rows3,
                                            len4 = len(rows4), rows4 = rows4)

#---------------------------------------------












#--------------------------------------------






@app.route("/finish")
def finish():
    return render_template("finish.html")




if __name__ == "__main__":
    app.run(debug=True)

