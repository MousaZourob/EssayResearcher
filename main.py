from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)   # Initializes app instance 

@app.route("/", methods=["POST", "GET"])    # Sets URL tag for home page and initializes HTTP protocols 
def home():                                 # Defines and renders home page
    if request.method == "POST":
        research = request.form["research"]
        key_word1 = request.form["keyword1"]
        key_word2 = request.form["keyword2"]
        key_word3 = request.form["keyword3"]
        return redirect(url_for("research", topic=research, word1=key_word1, word2=key_word2, word3=key_word3))
    else: 
        return render_template("home.html")

@app.route("/topic=<topic>+word1=<word1>+word2=<word2>+word3=<word3>")          # Sets URL tag for research page
def research(topic, word1, word2, word3):                                       # Defines and renders research page
    return render_template("research.html", content=[topic, word1, word2, word3])

if __name__ == "__main__":  # Runs website
    app.run(debug=True)