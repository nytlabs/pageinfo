import requests
from bs4 import BeautifulSoup
from HTMLParser import HTMLParseError
import json
import re
from urlparse import urlparse
from urlparse import urljoin

#get canonical
def get_canonical(url):
  canonical_url = ""
  response = requests.get(url)
  if response.status_code == 200:
    soup = BeautifulSoup(response.text)
    canonical = soup.find("link", rel="canonical")
    if canonical:
      canonical_url = canonical['href']
    else:
      og_url = soup.find("meta", property="og:url")
      canonical_url = og_url['content']
  return canonical_url

#get title, description, favicon, twitter card, facebook open graph data
def get_meta(url):

    
    data = {}
    data["title"] = ""
    data["description"] = None
    data["favicon"] = None
    data["facebook"] = {}
    data["twitter"] = {}

    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200: 
            soup = BeautifulSoup(response.text)

            #get title
            if soup.title.string:
                data["title"] = soup.title.string
            #get canonical
            canonical = soup.find("link", rel="canonical")
            if canonical:
                data["canonical"] = canonical['href']
            #get favicon
            parsed_uri = urlparse( url )
            if soup.find("link", rel="shortcut icon"):
                icon_rel = soup.find("link", rel="shortcut icon")["href"]
                icon_abs = urljoin( url, icon_rel )
                data["favicon"] = icon_abs
            else:
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
            # make sure canonical exists, use og as backup
            if not data['canonical'] or len(data['canonical']) == 0:
                if data['facebook'].has_key('og:url'):
                    data['canonical'] = data['facebook']['og:url']
            if not data['canonical'] or len(data['canonical']) == 0:
                data['canonical'] = url


            return json.dumps(data)
        else:
            return json.dumps({"canonical":url,"error":"URL returned status "+str(response.status_code)})
    except HTMLParseError:
        return json.dumps({"canonical":url,"error":"Error parsing page data"})
