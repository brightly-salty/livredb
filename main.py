from frontend import App
from backend import loadDB, saveDB
from data import DB

db = DB([])
saveDB(db)
db = loadDB()
app = App(db)
app.mainloop()
