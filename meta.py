from bs4 import BeautifulSoup
from HTMLParser import HTMLParseError
import requests
import json
import re
from urlparse import urlparse

def get_meta(url):
	data = {}
	data["title"] = ""
	data["description"] = None
	data["favicon"] = None
	data["facebook"] = {}
	data["twitter"] = {}

	try:
		if url is not None: #make sure we have a url
			page=requests.get(url)
			if page.status_code == 200: 
				soup = BeautifulSoup(page.text)
				
				#get title
				if soup.title.string:
					data["title"] = soup.title.string

				#get favicon
				parsed_uri = urlparse( url )
				domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
				data["favicon"] = domain + 'favicon.ico'

				#get description
				if soup.find('meta', attrs={'name':'description'}):
					data["description"] = soup.find('meta', attrs={'name':'description'})["content"]

				#get facebook open graph data
				if soup.findAll('meta', {"property":re.compile("^og")}):
					for tag in soup.findAll('meta', {"property":re.compile("^og")}):
						tag_type = tag['property']
						data["facebook"][tag_type] = tag['content']
						if tag_type == "og:description" and data["description"] is None:
							data["description"] = tag["content"]

				#get twitter card data
				if soup.findAll('meta', attrs={'name':re.compile("^twitter")}):
					for tag in soup.findAll('meta', attrs={'name':re.compile("^twitter")}):
						tag_type = tag['name']
						if 'content' in tag.attrs:
							data["twitter"][tag_type] = tag['content']
							if tag_type == "twitter:description" and data["description"] is None:
								data["description"] = tag["content"]

			#return error if status code is anything but 200
			else:
				data = "URL returned status %s" % page.status_code
		else:
			data = "No url provided"

	except HTMLParseError:
		data = "Error parsing page data"

	except:
		data = "Oops, something went wrong"


	return json.dumps(data)

