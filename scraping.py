from bs4 import BeautifulSoup
import requests

def raw_scraping(ville, nom, prenom):
	r = requests.get("https://www.google.fr/search?q={}+{}+{}".format(ville, nom, prenom))
	soup = BeautifulSoup(r.text, "html.parser")

	head3 = soup.find_all("h3", class_="r", limit=4)
	urls = []
	raw = ""

	for title in head3[1:]:
		link = title.a['href']
		urls.append(link.split('&')[0][7:])

	for url in urls:
		r = requests.get(url)
		soup = BeautifulSoup(r.text, "html.parser")
		string = soup.body.text
		raw += string

	return raw
