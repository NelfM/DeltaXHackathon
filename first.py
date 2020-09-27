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
        
        #------------------------------------------
        diff=pd.read_csv('diffsydiw.csv')
        sym=pd.read_csv('sym_t.csv')
        dia=pd.read_csv('dia_t.csv')
        #dia['idnr'] = dia['_id'].convert_objects(convert_numeric=True)
        sd_diff=diff.merge(sym, left_on='syd', right_on='syd')
        sd_diff=sd_diff.merge(dia, left_on='did', right_on='did')


        def read_data(filename):
            """ Reads in the last.fm dataset, and returns a tuple of a pandas dataframe
            and a sparse matrix of song/user/playcount """
            # read in triples of user/song/playcount from the input dataset
            data = pd.read_csv(filename,
                            usecols=[0, 1, 2],  # [36, 11, 10] vrk_pat_primkey,prd_atc_primkey,vdp_aantal
                            names=['user', 'song', 'plays'],
                            skiprows=1)  # [:1000000]   # user = patient, or prescriptionnr song=atc

            data = data.dropna(axis=0, how='any')  # drop nan
            data['plays'] = data['plays'] + 1
            # map each song and user to a unique numeric value
            data['user'] = data['user'].astype("category")
            data['song'] = data['song'].astype("category")

            # create a sparse matrix of all the users/plays
            plays = coo_matrix((data['plays'].astype(float),
                                (data['song'].cat.codes.copy(),
                                data['user'].cat.codes.copy())))

            return data, plays, data.groupby(['song']).plays.sum(), data['user'].cat.codes.copy()


        data, matrix, songsd, user = read_data('diffsydiw.csv')
        data.head(10)




        from sklearn.preprocessing import normalize


        def cosine(plays):
            normalized = normalize(plays)
            return normalized.dot(normalized.T)


        def bhattacharya(plays):
            plays.data = np.sqrt(plays.data)
            return cosine(plays)


        def ochiai(plays):
            plays = csr_matrix(plays)
            plays.data = np.ones(len(plays.data))
            return cosine(plays)


        def bm25_weight(data, K1=1.2, B=0.8):
            """ Weighs each row of the matrix data by BM25 weighting """
            # calculate idf per term (user)
            N = float(data.shape[0])
            idf = np.log(N / (1 + np.bincount(data.col)))

            # calculate length_norm per document (artist)
            row_sums = np.squeeze(np.asarray(data.sum(1)))
            average_length = row_sums.sum() / N
            length_norm = (1.0 - B) + B * row_sums / average_length

            # weight matrix rows by bm25
            ret = coo_matrix(data)
            ret.data = ret.data * (K1 + 1.0) / (K1 * length_norm[ret.row] + ret.data) * idf[ret.col]
            return ret


        def bm25(plays):
            plays = bm25_weight(plays)
            return plays.dot(plays.T)

        def get_largest(row, N=10):
            if N >= row.nnz:
                best = zip(row.data, row.indices)
            else:
                ind = np.argpartition(row.data, -N)[-N:]
                best = zip(row.data[ind], row.indices[ind])
            return sorted(best, reverse=True)


        def calculate_similar_artists(similarity, artists, artistid):
            neighbours = similarity[artistid]
            top = get_largest(neighbours)
            return [(artists[other], score, i) for i, (score, other) in enumerate(top)]


        #songsd = dict(enumerate(data['song'].cat.categories))
        user_count = data.groupby('user').size()
        #to_generate = sorted(list(songsd), key=lambda x: -user_count[x])

        similarity = bm25_weight(matrix)



        Ur, Si, VTr = svds(bm25_weight(coo_matrix(matrix)), k=100)
        VTr=pd.DataFrame(VTr)


        Sddf=pd.DataFrame(cosine_similarity(Ur,VTr.T),columns=user_count.index,index=list(songsd.index))
        Sddf.to_csv('Sddf.csv')

        Sydi=pd.DataFrame(cosine_similarity(Ur,VTr.T))

        booknr = int(x) # I call this once

        print()
        print("Your symptom is " + sym[sym['syd']==booknr]['symptom'][booknr-1])
        print()
        print('You may have one of the three following diseases:') #,Sddf[booknr].sort_values(ascending=False))
        print()
        list1= Sddf[booknr].sort_values(ascending=False).index
        count=0
        for i in list1[:3]:
            count += 1
            print(str(count) + ". " + dia[dia['did']==i].diagnose.values[0])
        #------------------------------------------

        
        return redirect(url_for("finish"))
    
    return render_template("symptoms.html", len1 = len(rows1), rows1 = rows1,
                                            len2 = len(rows2), rows2 = rows2,
                                            len3 = len(rows3), rows3 = rows3,
                                            len4 = len(rows4), rows4 = rows4)


#---------------------------------------------












#--------------------------------------------






@app.route("/finish", methods = ["POST", "GET"])
def finish():
    if request.method == "POST":
        req = request.form
        county = req["county"]
        
        counties = []

        with open('Covid Dataset.csv', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cases = {}
                for key in row:
                    cases.update({key : row[key]})

                counties.append(cases)
            
            y=int(cases[county])
            
        return render_template("finish.html", y=y)

    else:
        return render_template("finish.html")



if __name__ == "__main__":
    app.run(debug=True)

