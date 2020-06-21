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

def get_paragraphs(url, query, keywords):
	html_code = get_html_code(url)
	soup = BeautifulSoup(html_code, "html.parser")

	for paragraph in soup("p"):
		paragraph = " ".join(paragraph.get_text().split())

		if not paragraph == "" and (query in paragraph or
			any(kw in keywords for kw in paragraph)):

			if len(paragraph) > 200:
				paragraph = paragraph[:200] + " ..."
				
			return paragraph

def get_top_links(html_code):
	soup = BeautifulSoup(html_code, "html.parser")
	avoidLinks = tuple(["youtube.", "google."])
	links = []

	for div in soup.find_all("div", class_="BNeawe s3v9rd AP7Wnd"):
		div.decompose()

	for div in soup.find_all("div", class_="kCrYT"):

		for link in div.find_all("a"):
			currentLink = link.get("href")

			if not any(al in currentLink for al in avoidLinks):

				if "&sa=" in currentLink:
					currentLink = currentLink[7:currentLink.index("&sa=")]

				links.append(currentLink)
	return links

# BS4 Stuff
###########################################################################################
# Flask Stuff

app = Flask(__name__)   # Initializes app instance 
app.secret_key = "0RjiQhdtLs"
temp = "#"


@app.route("/", methods=["POST", "GET"])    # Sets URL tag for home page and initializes HTTP protocols 
@app.route("/#", methods=["POST", "GET"]) 
def home():                                 # Defines and renders home page
	if request.method == "POST":
		user_input = []
		
		topic = request.form["research"]
		user_input = request.form["keywords"].split(", ")

		user_input.insert(0, topic)

		check_empty = False
		for word in user_input:
			if not word:    
				check_empty =True

		if check_empty:
			flash("Fill in all the boxes!")
			return redirect(url_for("home"))

		return redirect(url_for("research", words=user_input))
	else: 
		return render_template("home.html")

@app.route("/<words>")                                      # Sets URL tag for research page
def research(words):                                        # Defines and renders research page
	paragraphs = []

	words = words.replace("\'", "")

	print(words)

	temp = words[1:len(words)-1].split(", ")

	print(temp)	

	topic = temp[0]
	keywords = temp[1:]

	print(topic)
	print(keywords)

	code_html = get_google_html(topic, keywords)
	links = get_top_links(code_html)

	for i in range(len(links)):
		paragraphs.append(get_paragraphs(links[i], topic, keywords))

	return render_template("research.html", content=paragraphs)	# Renders website

if __name__ == "__main__":  # Runs website
	app.run(debug=True)
