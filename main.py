from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)   # Initializes app instance 

@app.route("/", methods=["POST", "GET"])    # Sets URL tag for home page and initializes HTTP protocols 
def home():                                 # Defines and renders home page
    if request.method == "POST":
        research = request.form["research"]
        key_words = request.form["keywords"]
        return redirect(url_for("research", topic=research, words=key_words))
    else: 
        return render_template("home.html")

@app.route("/<topic>+<words>")          # Sets URL tag for research page
def research(topic, words):                         # Defines and renders research page
    return render_template("research.html")

if __name__ == "__main__":  # Runs website
    app.run(debug=True)