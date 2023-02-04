class Author:
  def __init__(self, name):
    splitted = name.split()
    if len(splitted) == 1:
      self.first = ""
      self.middle = ""
      self.last = splitted[0].strip()
    elif len(splitted) == 2:
      self.first = splitted[0].strip()
      self.middle = ""
      self.last = splitted[1].strip()
    elif len(splitted) == 3:
      self.first = splitted[0].strip()
      self.middle = splitted[1].strip()
      self.last = splitted[2].strip()
    else:
      print("ERROR:" + str(splitted))

  def getFirst(self):
    return self.first

  def getMiddle(self):
    return self.middle

  def getLast(self):
    return self.last
  
  def setFirst(self, first):
    self.first = first

  def setMiddle(self, middle):
    self.middle = middle

  def setLast(self, last):
    self.last = last

  def __str__(self):
    if self.first == "":
      return self.last
    elif self.middle == "":
      return self.first + " " + self.last
    else:
      return self.first + " " + self.middle + " " + self.last
      
class Title:
  def __init__(self, title):
    splitted = title.split(":", 1)
    self.main = splitted[0].strip()
    if len(splitted) > 1:
      self.sub = splitted[1].strip()
    else:
      self.sub = ""

  def getMain(self):
    return self.main

  def getSub(self):
    return self.sub

  def setMain(self, main):
    self.main = main

  def setSub(self, sub):
    self.sub = sub

  def __str__(self):
    if self.sub == "":
      return self.main
    else:
      return self.main + ": " + self.sub

class Book:
  def __init__(self, title, name):
    self.title = Title(title)
    self.authors = []
    self.author = Author(name)

  def getTitle(self):
    return str(self.title)

  def getAuthor(self):
    return str(self.author)

  def setTitle(self, title):
    self.title = title

  def setAuthor(self, author):
    self.author = author

class DB:
  def __init__(self, books):
    self.books = books

  def getBooks(self):
    return enumerate(self.books)

  def getBookById(self, id):
    return self.books[id]

  def setBookById(self, id, author, title):
    self.books[id] = Book(title, author)

  def addBook(self, author, title):
    self.books.append(Book(title, author))

