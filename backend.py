from urllib.parse import quote_plus
from urllib3 import PoolManager
from pickle import dump, load
from base64 import b64encode
from bs4 import BeautifulSoup

def loadDB(filename):
  return load(open(filename, 'rb'))

def saveDB(filename, db):
  with open(filename, 'wb') as file:
    dump(db, file)

def levenshteinDistance(s1, s2):
  if len(s1) > len(s2):
    s1, s2 = s2, s1
  distances = range(len(s1) + 1)
  for i2, c2 in enumerate(s2):
    distances_ = [i2+1]
    for i1, c1 in enumerate(s1):
      if c1 == c2:
        distances_.append(distances[i1])
      else:
        distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
    distances = distances_
  return distances[-1]

MAX_DISTANCE = 2

def isDuplicate(i, j):
  titleDistance = levenshteinDistance(i.getTitle().getMain(), j.getTitle().getMain())
  if titleDistance < MAX_DISTANCE:
    authorDistance = levenshteinDistance(i.getAuthor().getLast(), j.getAuthor().getLast())
    return authorDistance < MAX_DISTANCE
  else:
    return False

def findPossibleDuplicates(db):
  possibleDuplicates = []
  books = db.getBooks()
  for i in range(len(books)):
    for j in range(i, len(books)):
      if isDuplicate(i, j):
        possibleDuplicates.append((i, j))
  return possibleDuplicates

def getBiblioPrices(author, title):
  results = []
  http = PoolManager()
  url = "https://www.betterworldbooks.com/search/results?q=" + query
  r = http.request('GET', url)
  soup = BeautifulSoup(r.data, "html.parser")
  for searchResult in soup.find_all("div",_class="thumbnail"):
    link = "https://www.betterworldbooks.com/" + searchResult.find("a")["href"]
    price = searchResult.find("strong").text.split()[0][1:]
    shippingPrice = 0.99
    if price > 15.00:
      shippingPrice = 0.00
    results.append(link, price, shippingPrice)
  return results

def getURLs(book):
  # TODO: scrape prices, not just give URLs
  author = book.getAuthor().getFirst() + " " + book.getAuthor().getLast()
  title = book.getTitle().getMain()

  results = []
  http = PoolManager()
  
  # AbeBooks
  r = http.request('GET', "https://www.abebooks.com/servlet/SearchResults?sts=t&tn=" + quote_plus(title) + "&an=" + quote_plus(author))
  soup = BeautifulSoup(r.data, "html.parser")
  searchResults = soup.find("ul",id="srp-results")
  for searchResult in searchResults.find_all("li"):
    link = "https://www.abebooks.com" + searchResult.find("h2").find("a")["href"]
    price = int(searchResult.find("p",_class="item-price").text.split()[1])
    shippingPrice = int(searchResult.find("span",_class="item-shipping-price").text.split()[1])
    results.append(("AbeBooks", link, price, shippingPrice))

  # Alibris
  r = http.request('GET', "https://www.alibris.com/booksearch?mtype=B&author=" + quote_plus(author) + "&title=" + quote_plus(title))
  soup = BeautifulSoup(r.data, "html.parser")
  searchResults = soup.find("ul",id="works")
  for searchResult in searchResults.find_all("li"):
    link = "https://www.alibris.com" + searchResult.find("a",_class="button")["href"]
    price = int(searchResult.find("span",_class="price").text[1:])
    shippingPrice = 3.99
    results.append(("Alibris", link, price, shippingPrice))

  # BetterWorldBooks
  r = http.request('GET', "https://www.betterworldbooks.com/search/results?q=" + quote_plus(author + " " + title))
  soup = BeautifulSoup(r.data, "html.parser")
  for searchResult in soup.find_all("div",_class="thumbnail"):
    link = "https://www.betterworldbooks.com/" + searchResult.find("a")["href"]
    price = int(searchResult.find("strong").text.split()[0][1:])
    shippingPrice = 0.99
    if price > 15.00:
      shippingPrice = 0.00
    results.append(("BetterWorldBooks", link, price, shippingPrice))

  # Biblio
  r = http.request('GET', "https://www.biblio.com/search.php?author=" + quote_plus(author) + "&title=" + quote_plus(title))
  soup = BeautifulSoup(r.data, "html.parser")
  for searchResult in soup.find_all("div",_class="item"):
    link = searchResult.find("h2",_class="title").find("a")["href"]
    price = int(searchResult.find("span",_class="item-price").text[1:])
    shippingPrice = int(searchResult.find("div",_class="shipping").find("span").text[1:])
    results.append(("Biblio", link, price, shippingPrice))

  # HalfPriceBooks
  r = http.request('GET', "https://hpb.com/products?utf8=%E2%9C%93#" + b64encode(("{'filters':{'rareFind':false,'language':'ENG'},'type':'catalog::book','sort':'hpbUsedPrice:asc','keywords':'" + author + " " + title + "'','size':10,'from':0}").encode("utf8")))
  soup = BeautifulSoup(r.data, "html.parser")
  for searchResult in soup.find_all("div",_class="search-result"):
    link = "https://hpb.com" + searchResult.find("li",_class="title").find("a")["href"]
    price = int(searchResult.find("a",_class="font-medium").text.split()[-1][1:])
    shippingPrice = 3.99
    results.append(("HalfPriceBooks", link, price, shippingPrice))
    
  # Powell's Books
  r = http.request('GET', "https://www.powells.com/searchresults?keyword=" + quote_plus(author + " " + title))
  soup = BeautifulSoup(r.data, "html.parser")
  for searchResult in soup.find("ol",_class="booklist").find_all("li"):
    link = "https://wwww.powells.com" + searchResult.find("h3").find("a")["href"]
    price = int(searchResult.find("div",_class="reg-price").text[1:])
    shippingPrice = 5.99
    if price > 50.00:
      shippingPrice = 0.00
    results.append(("Powell's Books", link, price, shippingPrice))
    
  # ThriftBooks
  r = http.request('GET', "https://www.thriftbooks.com/browse/?b.search=" + quote_plus(author + " " + title) + "#b.s=topMatches-desc&b.p=1&b.pp=30&b.oos&b.tile")
  soup = BeautifulSoup(r.data, "html.parser")
  for searchResult in soup.find_all("div",_class="Recipe-default"):
    link = "https://wwww.thriftbooks.com" + searchResult.find("a")["href"]
    price = int(searchResult.find("div",_class="SearchResultListItem-dollarAmount").text)
    shippingPrice = 1.49
    if price > 15.00:
      shippingPrice = 0.00
    results.append(("ThriftBooks", link, price, shippingPrice))
  
  return results