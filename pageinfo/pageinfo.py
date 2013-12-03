from bs4 import BeautifulSoup
from HTMLParser import HTMLParseError
import tornado.httpclient
import json
import re
from urlparse import urlparse
from urlparse import urljoin
import functools

#get title, description, favicon, twitter card, facebook open graph data
def get_meta(url, handler):

  if url is not None:
    callback = functools.partial(parse_html, handler=handler, url=url)
    http_client = tornado.httpclient.AsyncHTTPClient() 
    http_client.fetch(url, callback)

  else:
    handler.write("something went wrong")
    handler.finish()

def parse_html(response, handler, url):

  data = {}
  data["title"] = ""
  data["description"] = None
  data["favicon"] = None
  data["facebook"] = {}
  data["twitter"] = {}

  try:
    if response.code == 200: 
        soup = BeautifulSoup(response.body)

        #get title
        if soup.title.string:
          data["title"] = soup.title.string

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

        handler.write(json.dumps(data))

    else:
      handler.write( "URL returned status %s" % response.code)

  except HTMLParseError:
    handler.write( "Error parsing page data" )

  handler.finish()




