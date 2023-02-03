from enum import Enum, auto

class Status(Enum):
  DONE = auto()
  STARTED = auto()
  ACQUIRED = auto()
  INTERESTED = auto()

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
    splitted = title.split(":")
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
  def __init__(self, title, name, status):
    self.title = Title(title)
    self.authors = []
    self.author = Author(name)
    self.status = status

  def getTitle(self):
    return self.title

  def getAuthor(self):
    return self.author

  def getStatus(self):
    return self.status

  def setTitle(self, title):
    self.title = title

  def setAuthor(self, author):
    self.author = author

  def setStatus(self, status):
    self.status = status

class DB:
  def __init__(self, books):
    self.books = books

  def getBooks(self):
    return self.books

  def setBooks(self, books):
    self.books = books

  def getBookById(self, id):
    return self.books[id]

  def setBookAtId(self, title, author):
    self.books[id] = Book(title, author)

  def getBooksByStatus(self, status):
    result = []
    for (i, book) in enumerate(self.books):
      if book.getStatus() is status:
        result.append((i, book))
    return result

  def getDoneBooks(self):
    return self.getBooksByStatus(Status.DONE)

  def getStartedBooks(self):
    return self.getBooksByStatus(Status.STARTED)

  def getAcquiredBooks(self):
    return self.getBooksByStatus(Status.ACQUIRED)

  def getInterestedBooks(self):
    return self.getBooksByStatus(Status.INTERESTED)

  def addInterestedBook(self, title, author):
    self.books.append(Book(title, author, Status.INTERESTED))

  def addAcquiredBook(self, title, author):
    self.books.append(Book(title, author, Status.ACQUIRED))

  def addStartedBook(self, title, author):
    self.books.append(Book(tite, author, Status.STARTED))

  def addDoneBook(self, title, author):
    self.books.append(Book(title, author, Status.DONE))
    