from flask import Flask, redirect, url_for, render_template, request
app = Flask(__name__)

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

        print(name, email, symp)

        return redirect(url_for("finish"))
    return render_template("login.html")

@app.route("/finish")
def finish():
    return render_template("finish.html")





if __name__ == "__main__":
    app.run(debug=True)
