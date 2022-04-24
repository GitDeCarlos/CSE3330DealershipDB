from cgitb import text
import tkinter as tk
import mysql.connector

# global variables
_font = "Raleway"
_color1 = "#26d38e"
_color2 = "black"

# main window configuration
window = tk.Tk()
window.title("DealershipDB Interface")
window.geometry("720x480")
window.resizable(False, False)
window.configure(background=_color1)
window.option_add("*Font", _font)

# connecting the mySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="dealershipdb"
)
cursor = mydb.cursor()

# function definitions

def getQuery(query="SELECT * FROM CUSTOMER"):
    cursor.execute(query)
    result = cursor.fetchall()
    resultText = ""
    for x in result:
        resultText += str(x) + "\n"
    return resultText

def insertCustomer():
    
    def confirmCustomer():
        name = nameentry.get()
        phone = phoneentry.get()

        clearAll()
        query = "INSERT INTO CUSTOMER (Name, Phone) VALUES ('{name}', '{phone}')".format(name=name, phone=phone)
        getQuery(query)
        queryText.insert(tk.INSERT, "New Customer Added.")
        
        top.destroy()

    top = tk.Toplevel(window)
    top.title("Insert Customer")
    top.geometry("300x120")
    top.resizable(False, False)
    top.configure(background=_color1)

    # TODO: name label/entry, phone label/entry, confirm button
    titlelabel = tk.Label(top, text="Insert Customer info into DB", background=_color1)
    titlelabel.grid(column=0, columnspan=2, row=0)

    namelabel = tk.Label(top, text="Full Name", background=_color1)
    namelabel.grid(column=0, row=1)
    nameentry = tk.Entry(top)
    nameentry.grid(column=1, row=1)

    phonelabel = tk.Label(top, text="Phone Number", background=_color1)
    phonelabel.grid(column=0, row=2)
    phoneentry = tk.Entry(top)
    phoneentry.grid(column=1, row=2)

    confirmbutton = tk.Button(top, text="Confirm", command=confirmCustomer)
    confirmbutton.grid(column=0, columnspan=2, row=3)

def executeQuery():
    query = queryText.get("1.0", tk.END)

    clearAll()
    queryText.insert(tk.INSERT, getQuery(query))

def printAll():
    clearAll()
    queryText.insert(tk.INSERT, getQuery())

def clearAll():
    queryText.delete("1.0", tk.END)

# ------- GUI START -------
contentFrame = tk.Frame(window, height=480, width=700, background=_color2)
contentFrame.pack(side=tk.LEFT)

queryText = tk.Text(contentFrame)
queryText.pack(fill=tk.BOTH)


# menubar elements
menubar = tk.Menu(window)

querymenu = tk.Menu(menubar, tearoff=0)
querymenu.add_command(label="Print", command=printAll)
querymenu.add_command(label="Execute Query", command=executeQuery)
querymenu.add_command(label="Clear Query", command=clearAll)
querymenu.add_separator()
querymenu.add_command(label="Exit", command=window.quit)

editmenu = tk.Menu(menubar, tearoff=0)
editmenu.add_command(label="Insert Customer", command=insertCustomer)
editmenu.add_command(label="Insert Vehicle")

menubar.add_cascade(label="Query", menu=querymenu)
menubar.add_cascade(label="Edit", menu=editmenu)

# display window
window.config(menu=menubar)
window.mainloop()
