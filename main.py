from flask import Flask, redirect, url_for, render_template, request, flash
from bs4 import BeautifulSoup
from requests import get

def get_html_code(url):
	return get(url).text

def get_google_html(query, keywords):
	query = query.replace(" ", "+")
	url = f"https://google.com/search?q={query}"

	if keywords:
		for word in keywords:
			url += f"+\"{word}\"+OR"
		url = url[:-3]

	return get_html_code(url)

def get_paragraphs(url):
	html_code = get_html_code(url)
	soup = BeautifulSoup(html_code, "html.parser")
	paragraphs = []

	for paragraph in soup("p"):
		paragraph = " ".join(paragraph.get_text().split())
		if not paragraph == "":
			paragraphs.append(paragraph)

	return paragraphs

def get_top_links(html_code):
	soup = BeautifulSoup(html_code, "html.parser")
	avoidLinks = tuple(["https://www.youtube", "http://scholar.google"])
	links = []

	for div in soup.find_all("div", class_="BNeawe s3v9rd AP7Wnd"):
		div.decompose()

	for div in soup.find_all("div", class_="kCrYT"):
		for link in div.find_all("a"):
			currentLink = link.get("href")
			if "&sa=" in currentLink and not any(al in currentLink for al in avoidLinks):
				links.append(currentLink[7:currentLink.index("&sa=")])

	return links

query = "gambling addiction"
keywords = ["drug", "crime"]
links = get_top_links(get_google_html(query, keywords))
for link in links:
	print(link)

# BS4 Stuff
###########################################################################################
# Flask Stuff

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