from flask import Flask, redirect, url_for, render_template, request, flash

app = Flask(__name__)   # Initializes app instance 
app.secret_key = "0RjiQhdtLs"

@app.route("/", methods=["POST", "GET"])    # Sets URL tag for home page and initializes HTTP protocols 
def home():                                 # Defines and renders home page
    if request.method == "POST":
        topic = request.form["research"]
        keyword1 = request.form["keyword1"]
        keyword2 = request.form["keyword2"]
        keyword3 = request.form["keyword3"]
        user_input = [topic, keyword1, keyword2, keyword3]
        
        check_empty = False
        for word in user_input:
            if not word:
                check_empty =True

        if check_empty:
            flash("Fill in all the boxes!")
            return redirect(url_for("home"))

        return redirect(url_for("research", words=list(user_input)))
    else: 
        return render_template("home.html")

@app.route("/<words>")                                     # Sets URL tag for research page
def research(words):                                       # Defines and renders research page
    return render_template("research.html", content=list(words))

if __name__ == "__main__":  # Runs website
    app.run(debug=True)