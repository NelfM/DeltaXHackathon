from flask import Flask, redirect, url_for, render_template, request
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse.linalg import svds
from sklearn.preprocessing import LabelEncoder
from tqdm import tqdm
from scipy.sparse import coo_matrix, csr_matrix
from subprocess import check_output


app = Flask(__name__)


def diseaseFromSymptoms(i):






@app.route("/")
def home():
    return render_template("index.html", content="Testing")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        req = request.form 
        name = req["fullname"]
        email = req["email"]
        symp = req["symptoms"]

        return redirect(url_for("finish"))
    return render_template("login.html")

@app.route("/finish")
def finish():
    return render_template("finish.html")

if __name__ == "__main__":
    app.run(debug=True)
