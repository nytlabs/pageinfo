pageinfo
====

pageinfo is a simple module for extracting information from web pages. Currently, pageinfo will return the following from a url, where available:

* Canonical
* Title
* Description
* Favicon
* Twitter card data
* Facebook Open Graph data


##installation

`pip install pageinfo`

##usage

```python
import pageinfo
pageinfo.get_meta('http://www.myurl.com')
```
The first argument is the url you want to get info for and the second argument is the handler that is making the request (this assues pageinfo is being requested by a tornado server). The handler is required so that multiple requests can be made concurrently in a non-blocking fashion.

The above code will return a dict with the available page information. Here's a sample response for `http://bits.blogs.nytimes.com/2013/11/20/a-gift-from-steve-jobs-returns-home`:

```javascript
{   
    "canonical":"http://bits.blogs.nytimes.com/2013/11/20/a-gift-from-steve-jobs-returns-home/" 
    "twitter": {    
        "twitter:title": "A Gift From Steve Jobs Returns Home",
        "twitter:image": "http://graphics8.nytimes.com/images/2013/11/18/technology/bits-brilliant-jobs/bits-brilliant-jobs-thumbLarge.jpg",
        "twitter:description": "An Apple II that spent the last 33 years in Katmandu, Nepal, most of it packed away in a hospital basement there, was a rare symbol of the charity of Steven P. Jobs.", 
        "twitter:url": "http://bits.blogs.nytimes.com/2013/11/20/a-gift-from-steve-jobs-returns-home/"
    },

    "favicon": "http://bits.blogs.nytimes.com/favicon.ico",

    "facebook": {    
        "og:url": "http://bits.blogs.nytimes.com/2013/11/20/a-gift-from-steve-jobs-returns-home/",
        "og:site_name": "Bits Blog",
        "og:type": "article",
        "og:description": "An Apple II that spent the last 33 years in Katmandu, Nepal, most of it packed away in a hospital basement there, was a rare symbol of the charity of Steven P. Jobs.", 
        "og:title": "A Gift From Steve Jobs Returns Home",
        "og:image": "http://graphics8.nytimes.com/images/2013/11/18/technology/bits-brilliant-jobs/bits-brilliant-jobs-videoSixteenByNine600.jpg"
    },

    "description": "An Apple II that spent the last 33 years in Katmandu, Nepal, most of it packed away in a hospital basement there, was a rare symbol of the charity of Steven P. Jobs.", 

    "title": "A Gift From Steve Jobs Returns Home - NYTimes.com"
    }   
```
