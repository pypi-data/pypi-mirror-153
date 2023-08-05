from urllib.request import Request, urlopen
from lxml import etree, html

def get_html(url): 
    # get the html of the url 
    hdr = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
        "Accept-Encoding": "none",
        "Accept-Language": "en-US,en;q=0.8",
        "Connection": "keep-alive",
    }

    req = Request(url, headers=hdr)
    page = urlopen(req)
    result = page.read()
    return result

def pretty_html(web_html): 
    # pretty print the html page 
    document_root = html.fromstring(web_html)
    print(etree.tostring(document_root, encoding='unicode', pretty_print=True))


if __name__ == '__main__': 
    url = "https://eecs.berkeley.edu/"
    web_html = get_html(url)
    pretty_html(web_html)    
