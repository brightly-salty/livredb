import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from backend import saveDB

class App(tk.Tk):
  def __init__(self, db):
    self.db = db
    super().__init__()

    self.title("LivreDB")
    self.geometry("800x500")
    self.display_books()
    self.bookFrame.grid()

  def display_books(self):
    self.bookFrame = ttk.Frame(self)

    r = 1
    for (id, book) in self.db.getBooks():
      text = book.getTitle() + " by " + book.getAuthor()
      label = ttk.Label(self.bookFrame, text=text)
      label.grid(row = r, column = 0)
      button = ttk.Button(self.bookFrame, text="Edit")
      button['command'] = lambda: self.edit_book(id)
      button.grid(row = r, column = 1)
      r += 1

    add_button = ttk.Button(self.bookFrame, text="Add a book")
    add_button['command'] = self.add_book_clicked
    add_button.grid(row = r, column = 0, columnspan = 2)

  def create_book_entries(self, frame, callback):
    authorLabel = ttk.Label(frame,text="Author:")
    authorLabel.grid(row=0, column = 0)
    authorEntry = ttk.Entry(frame, textvariable=self.authorVar)
    authorEntry.grid(row=0, column = 1)
    titleLabel = ttk.Label(frame, text="Title:")
    titleLabel.grid(row=1,column=0)
    titleEntry = ttk.Entry(frame, textvariable=self.titleVar)
    titleEntry.grid(row=1,column=1)
    saveButton = ttk.Button(frame, text="Save")
    saveButton["command"] = callback
    saveButton.grid(row=3,column=0,columnspan=2)

  def edit_book(self, id):
    book = self.db.getBookById(id)
    self.viewFrame = ttk.Frame(self)
    self.authorVar = tk.StringVar(self.viewFrame)
    self.authorVar.set(book.getAuthor())
    self.titleVar = tk.StringVar(self.viewFrame)
    self.titleVar.set(book.getTitle())
    self.create_book_entries(self.viewFrame, lambda: self.save_edited_book(id))
    self.bookFrame.grid_forget()
    self.viewFrame.grid()

  def save_edited_book(self, id):
    newAuthor = self.authorVar.get()
    newTitle = self.titleVar.get()
    self.db.setBookById(id, newAuthor, newTitle)
    saveDB(self.db)
    self.display_books()
    self.viewFrame.grid_forget()
    self.bookFrame.grid()

  def add_book_clicked(self):
    self.addFrame = ttk.Frame(self)
    self.authorVar = tk.StringVar(self.addFrame)
    self.titleVar = tk.StringVar(self.addFrame)
    self.create_book_entries(self.addFrame, self.save_added_book)
    self.bookFrame.grid_forget()
    self.addFrame.grid()
  
  def save_added_book(self):
    author = self.authorVar.get()
    title = self.titleVar.get()
    self.db.addBook(author, title)
    saveDB(self.db)
    self.display_books()
    self.addFrame.grid_forget()
    self.bookFrame.grid()