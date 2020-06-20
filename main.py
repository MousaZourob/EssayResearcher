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
        keywords = [keyword1, keyword2, keyword3]
        if len(topic) == 0 or len(keyword1) == 0 or len(keyword2) == 0 or len(keyword3) == 0:
            flash("Fill in all the boxes!")
            return redirect(url_for("home"))
    
        return redirect(url_for("research", topic=topic, word1=keyword1, word2=keyword2, word3=keyword3))
    else: 
        return render_template("home.html")

@app.route("/topic=<topic>+word1=<word1>+word2=<word2>+word3=<word3>")          # Sets URL tag for research page
def research(topic, word1, word2, word3):                                       # Defines and renders research page
    return render_template("research.html", content=[topic, word1, word2, word3])

if __name__ == "__main__":  # Runs website
    app.run(debug=True)