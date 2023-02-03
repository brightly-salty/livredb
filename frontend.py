import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

class App(tk.Tk):
  def __init__(self, db):
    self.db = db
    super().__init__()

    self.title("LivreDB")
    self.geometry("400x300")
    self.display_books()

  def display_books(self):
    self.interestedLabel = ttk.Label(self, text="Interested")
    self.interestedLabel.grid(row = 0, column = 0, columnspan = 2)

    r = 1
    
    self.interestedBookLabels = {}
    for (id, book) in self.db.getInterestedBooks():
      s = str(book.getTitle()) + " by " + str(book.getAuthor())
      label = ttk.Label(self, text=s)
      label.grid(row = r, column = 0)
      r += 1
      self.interestedBookLabels[str(id)] = label

    self.acquiredLabel = ttk.Label(self, text="Acquired")
    self.acquiredLabel.grid(row = r, column = 0, columnspan = 2)
    r += 1
    
    self.acquiredBookLabels = {}
    for (id, book) in self.db.getAcquiredBooks():
      s = str(book.getTitle()) + " by " + str(book.getAuthor())
      label = ttk.Label(self, text=s)
      label.grid(row = r, column = 0)
      button = ttk.Button(self, text="View")
      button[command] = lambda : view_interested_book(id)
      button.grid(row = r, column = 1)
      r += 1
      self.acquiredBookLabels[str(id)] = label

    self.startedLabel = ttk.Label(self, text="Interested")
    self.startedLabel.grid(row = r, column = 0, columnspan = 2)
    r += 1
    
    self.startedBookLabels = {}
    for (id, book) in self.db.getStartedBooks():
      s = str(book.getTitle()) + " by " + str(book.getAuthor())
      label = ttk.Label(self, text=s)
      label.grid(row = r, column = 0)
      r += 1
      self.startedBookLabels[str(id)] = label
      
    self.doneLabel = tk.Label(text="Done")
    self.doneLabel.grid(row = r, column = 0, columnspan = 2)
    r += 1
    
    self.doneBookLabels = {}
    for (id, book) in self.db.getDoneBooks():
      s = str(book.getTitle()) + " by " + str(book.getAuthor())
      label = ttk.Label(self, text=s)
      label.grid(row = r, column = 0)
      r += 1
      self.doneBookLabels[str(id)] = label
    
    self.button = ttk.Button(self, text="Add a book")
    self.button['command'] = self.add_book_clicked
    self.button.grid(row = r, column = 0, columnspan = 2)
    r += 1

  def view_interested_book(self, id):
    _label = self.interestedBookLabels[str(id)]
    _book = self.db.getBookById(id)
    frame = ttk.Frame(self)
    author = ttk.StringVar()
    author.set(str(book.getAuthor()))
    title = ttk.StringVar()
    author.set(str(book.getTitle()))
    authorLabel = ttk.Label(frame,text="Author:")
    authorLabel.grid(row=0, column = 0)
    authorEntry = ttk.Entry(frame, textvariable=author)
    authorEntry.grid(row=0, column = 1)
    titleLabel = ttk.Label(frame, text="Title:")
    titleLabel.grid(row=1,column=0)
    titleEntry = ttk.Entry(frame, textvariable=title)
    titleEntry.grid(row=1,column=1)

  def add_book_clicked(self):
    showinfo(title="Information", message="Add a book!")
  
    