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

			if len(paragraph) > 300:
				paragraph = paragraph[:300] + " ..."
				
			return paragraph

def get_top_links(html_code, choices):
	soup = BeautifulSoup(html_code, "html.parser")
	avoidLinks = tuple(["youtube.", "google."])
	links = []
	suffixChoices = tuple([".edu", ".org", ".gov"])

	for div in soup.find_all("div", class_="BNeawe s3v9rd AP7Wnd"):
		div.decompose()

	choices = choices[1:-1]
	choices = choices.split(", ")

	if "True" in choices:
		for div in soup.find_all("div", class_="kCrYT"):

			for link in div.find_all("a"):
				currentLink = link.get("href")

				for i in range(len(choices)):
					if choices[i] == "True":
						if suffixChoices[i] in currentLink:
							if not any(al in currentLink for al in avoidLinks):

								if "&sa=" in currentLink:
									currentLink = currentLink[7:currentLink.index("&sa=")]

								links.append(currentLink)
	else:
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
@app.route("/#", methods=["POST", "GET"]) 	# Second route to not display landing page twice
def home():                                 # Defines and renders home page
	if request.method == "POST":			# If request method is post go to research page
		user_input = []		# Initializes user input list
		choices_list = []

		topic = request.form["research"]	# Gets topic from form
		user_input = request.form["keywords"].split(", ")	# Gets keywords from keywords box
		
		choices_list.append(request.form.getlist('option1'))	# Gets extra options
		choices_list.append(request.form.getlist('option2'))	
		choices_list.append(request.form.getlist('option3'))	

		for i in range(len(choices_list)):
			if (choices_list[i] == ["on"]):
				choices_list[i] = True
			else:
				choices_list[i] = False

		user_input.insert(0, topic)		# Combines topic and keywords into 1 list

		check_empty = False		# Checks if all boxes have been filled or not 
		for word in user_input:		# Goes through every word to make sure they're all full
			if not word:    
				check_empty =True

		if check_empty:		# If they're not full flashes a message asking to fill in all the boxes
			flash("Fill in all the boxes!")
			return redirect(url_for("home"))

		return redirect(url_for("research", words=user_input, choices=choices_list))	# Redirects user to research page to see results
	else: 
		return render_template("home.html")		# If request is a GET take them to home page to enter data

@app.route("/<words>+<choices>")                                      # Sets URL tag for research page
def research(words, choices):                                         # Defines and renders research page
	paragraphs = []

	words = words.replace("\'", "")				# Removes ' from words after it gets converted to string
	temp = words[1:len(words)-1].split(", ")	# Removes [] and splits it into a list

	topic = temp[0]			# Gets topic which equals first index in temp
	keywords = temp[1:]		# Gets keywords from temp list

	code_html = get_google_html(topic, keywords)	# Gets HTML code
	links = get_top_links(code_html, choices)		# Sends HTML code to get top links

	for i in range(len(links)):		# Gets paragraphs using links
		paragraphs.append(get_paragraphs(links[i], topic, keywords))	# Adds paragraphs to paragraphs list

	check = True	# Checks if paragraphs is empty
	for paragraph in paragraphs:	# Goes through every paragraph to check if its empty
		if not paragraph == None:
			check = False

	if check:	# If it empty flashes message 
		flash("Add more keywords!")

	return render_template("research.html", content=paragraphs, webpages=links)	# Renders research page

if __name__ == "__main__":  # Runs website
	app.run(debug=True)
