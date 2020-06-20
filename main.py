from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)   # Initializes app instance 

@app.route("/", methods=["POST", "GET"])    # Sets URL tag for home page and initializes HTTP protocols 
def home():                                 # Defines and renders home page
    if request.method == "POST":
        research = request.form["research"]
        key_words = request.form["keywords"]
        return redirect(url_for("research", topic=research))
    else: 
        return render_template("home.html")

@app.route("/<topic>")         # Sets URL tag for research page
def research(topic):     # Defines and renders research page
    return f"<h1>{topic}</h1>"

if __name__ == "__main__":  # Runs website
    app.run(debug=True)