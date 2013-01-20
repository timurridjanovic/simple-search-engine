index = {}

def get_page(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ""

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)


def get_all_links(page):
    links = []
    while True:
        url,endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def crawl_web(seed, max_depth):
    tocrawl = [seed]
    crawled = []
    next_depth = []
    depth = 0
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled and depth <= max_depth:
            content = get_page(page)
            add_page_to_index(index, page, content)
            union(next_depth, get_all_links(get_page(page)))
            crawled.append(page)
        if not tocrawl:
            tocrawl, next_depth = next_depth, []
            depth = depth + 1
    return index


def add_to_index(index, keyword, url):
   if keyword in index:
      index[keyword].append(url)
   else:
      index[keyword] = [url]

def add_page_to_index(index,url,content):
    l = content.split()
    for e in l:
        add_to_index(index, e, url)

def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    return None


print crawl_web("http://www.udacity.com/cs101x/index.html",0)


print crawl_web("http://www.udacity.com/cs101x/index.html",1)


#print crawl_web("http://www.udacity.com/cs101x/index.html",50)


#(May be in any order)

print lookup(index, '<body>')




