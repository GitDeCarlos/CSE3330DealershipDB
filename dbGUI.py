from cgitb import text
import tkinter as tk
import datetime as datetime
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
    rows = 0
    for x in result:
        resultText += str(x) + "\n"
        rows += 1
    resultText += str(rows) + " rows returned from query.\n"
    return resultText

def cleaner(words):
    words = words.replace("(", "")
    words = words.replace(")", "")
    words = words.replace("'", "")
    words = words.replace(",", "")
    words = words.split('\n')
    return words[0]

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
 
def insertVehicle():
    
    def confirmVehicle():
        vehicleID = videntry.get()
        description = descentry.get()
        year = yearentry.get()
        type = typeentry.get()
        category = categoryentry.get()

        clearAll()
        query = "INSERT INTO VEHICLE (VehicleID, Description, Year, Type, Category) VALUES ('{vehicleID}', '{description}', '{year}','{type}','{category}')".format(vehicleID=vehicleID, description=description, year=year, type=type, category=category)
        getQuery(query)
        queryText.insert(tk.INSERT, "New Vehicle Added.")
        
        top.destroy()

    top = tk.Toplevel(window)
    top.title("Insert Vehicle")
    top.geometry("300x180")
    top.resizable(False, False)
    top.configure(background=_color1)

    # TODO: name label/entry, phone label/entry, confirm button
    titlelabel = tk.Label(top, text="Insert Customer info into DB", background=_color1)
    titlelabel.grid(column=0, columnspan=2, row=0)

    vidlabel = tk.Label(top, text="Vehicle ID", background=_color1)
    vidlabel.grid(column=0, row=1)
    videntry = tk.Entry(top)
    videntry.grid(column=1, row=1)

    desclabel = tk.Label(top, text="Description", background=_color1)
    desclabel.grid(column=0, row=2)
    descentry = tk.Entry(top)
    descentry.grid(column=1, row=2)

    yearlabel = tk.Label(top, text="Year", background=_color1)
    yearlabel.grid(column=0, row=3)
    yearentry = tk.Entry(top)
    yearentry.grid(column=1, row=3)

    typelabel = tk.Label(top, text="Type", background=_color1)
    typelabel.grid(column=0, row=4)
    typeentry = tk.Entry(top)
    typeentry.grid(column=1, row=4)

    categorylabel = tk.Label(top, text="Category", background=_color1)
    categorylabel.grid(column=0, row=5)
    categoryentry = tk.Entry(top)
    categoryentry.grid(column=1, row=5)

    confirmbutton = tk.Button(top, text="Confirm", command=confirmVehicle)
    confirmbutton.grid(column=0, columnspan=2, row=6)

def newRental():
    def process():
        name = nameentry.get()
        StartDate = sDateentry.get()
        OrderDate = datetime.date.today().strftime('%Y-%m-%d')
        VehicleType = typeMenu.get()
        VehicleCategory = catMenu.get()
        RentalType = rtMenu.get()
        ReturnDate = eDateentry.get()
        #get customerid
        query = "SELECT CustID FROM Customer WHERE Name = '{}'".format(name)
        cust = getQuery(query)
        if cust == '':
            queryText.insert(tk.INSERT,"No Customer Found")
            return
        cust = cleaner(cust)
        queryText.insert(tk.INSERT,"Customer ID: " + cust + '\n')

        # Get key value for rental type
        if VehicleType == 'Compact': 
            VehicleType = 1
        elif VehicleType == 'Medium': 
            VehicleType = 2
        elif VehicleType == 'Large': 
            VehicleType = 3
        elif VehicleType == 'SUV': 
            VehicleType = 4
        elif VehicleType == 'Truck': 
            VehicleType = 5
        elif VehicleType == 'VAN': 
            VehicleType = 6
        
        # Get category key
        if VehicleCategory == 'Basic': 
            VehicleCategory = 0
        elif VehicleCategory == 'Luxury': 
            VehicleCategory = 1

        # Get Rental Type key
        if RentalType == 'Daily': 
            RentalType = 1
        elif RentalType == 'Weekly': 
            RentalType = 7

        # Find a free vehicle of specified type and category
        query = "SELECT VehicleID FROM Vehicle WHERE Type = {} AND Category = {} AND VehicleID NOT IN (SELECT VehicleID FROM rental WHERE Returned = 1)".format(RentalType, VehicleCategory)
        vehicleID = getQuery(query)
        # Check For Return if not close
        if vehicleID == '':
            queryText.insert(tk.INSERT,"No Vehicle Found")
            return
        # Clean Data Display and turn to int
        vehicleID = cleaner(vehicleID)
        queryText.insert(tk.INSERT,"Vehicle ID: " + vehicleID + '\n')

        # Calculate qautity and rate
        start = datetime.datetime.strptime(StartDate, '%Y-%m-%d')
        start = start.date()
        end = datetime.datetime.strptime(ReturnDate, '%Y-%m-%d').date()
        Qty = (end - start)
        if RentalType == 1:
            Qty = Qty.days 
            query = "SELECT Daily FROM rate WHERE Type = {} AND Category = {}".format(RentalType, VehicleCategory)
            rate = getQuery(query)
        if RentalType == 7:
            Qty = Qty.days / 7
            query = "SELECT Weekly FROM rate WHERE Type = {} AND Category = {}".format(RentalType, VehicleCategory)
            rate = getQuery(query)
        if rate == '':
            queryText.insert(tk.INSERT,"No Rate Found")
            return
        rate = cleaner(rate)
        queryText.insert(tk.INSERT,"Vehicle Rate: " + rate + "\n")
        rate = int(rate)

        TotalAmount = rate * Qty
        queryText.insert(tk.INSERT,"Total: " + str(TotalAmount) + "\n")
        PaymentDate = "0000-00-00"

        #clearAll()
        #query = "INSERT INTO RENTAL (CustID, VehicleID, StartDate, OrderDate, RentalType, Qty, ReturnDate, TotalAmount, PaymentDate) VALUES ({cust}, '{VehicleID}', '{StartDate}', '{OrderDate}', '{RentalType}', {Qty}, '{ReturnDate}', {TotalAmount}, '{PaymentDate}')"
        query = "INSERT INTO rental (CustID, VehicleID, StartDate, OrderDate, RentalType, Qty, ReturnDate, TotalAmount, PaymentDate) VALUES ({cust}, '{VehicleID}', '{StartDate}', '{OrderDate}', {RentalType}, {Qty}, '{ReturnDate}', {TotalAmount}, '{PaymentDate}')".format(cust=cust, VehicleID=vehicleID, StartDate=StartDate, OrderDate=OrderDate, RentalType=RentalType, Qty=Qty, ReturnDate=ReturnDate, TotalAmount=TotalAmount, PaymentDate=PaymentDate)
        getQuery(query)
        queryText.insert(tk.INSERT, "New Customer Added.")
        
        top.destroy()

    top = tk.Toplevel(window)
    top.title("New Rental")
    top.geometry("480x480")
    top.resizable(False, False)
    top.configure(background=_color1)

    titlelabel = tk.Label(top, text="Insert Customer info into DB", background=_color1)
    titlelabel.grid(column=0, columnspan=2, row=0)

    namelabel = tk.Label(top, text="Full Name", background=_color1)
    namelabel.grid(column=0, row=1)
    nameentry = tk.Entry(top)
    nameentry.grid(column=1, row=1)

    sDateLabel = tk.Label(top, text="Start Date (YYYY-MM-DD)", background=_color1)
    sDateLabel.grid(column=0, row=3)
    sDateentry = tk.Entry(top)
    sDateentry.grid(column=1, row=3)

    eDateLabel = tk.Label(top, text="End Date (YYYY-MM-DD)", background=_color1)
    eDateLabel.grid(column=0, row=4)
    eDateentry = tk.Entry(top)
    eDateentry.grid(column=1, row=4)

    #TYPE MENU
    # Dropdown menu options
    typeDict = ['Compact','Medium','Large','SUV','Truck','VAN']
    # datatype of menu text
    typeMenu = tk.StringVar()
    # initial menu text
    typeMenu.set( "Select a Vehicle Type" )
    # Create Dropdown menu
    Typedrop = tk.OptionMenu( top , typeMenu , *typeDict)
    Typedrop.grid(column=0, row=5)
    #Typedrop.pack()

    #CATEGORY MENU
    # Dropdown menu options
    catDict = ['Basic','Luxury']
    # datatype of menu text
    catMenu = tk.StringVar()
    # initial menu text
    catMenu.set( "Select a Vehicle Category" ) 
    # Create Dropdown menu
    catdrop = tk.OptionMenu( top , catMenu , *catDict)
    catdrop.grid(column=0, row=6)
   # catdrop.pack()

    #RENTAL TYPE MENU
    # Dropdown menu options
    rtDict = ['Daily','Weekly']
    # datatype of menu text
    rtMenu = tk.StringVar()
    # initial menu text
    rtMenu.set( "Select a Rental Type" ) 
    # Create Dropdown menu
    rtdrop = tk.OptionMenu( top , rtMenu , *rtDict)
    rtdrop.grid(column=0, row=7)
    #rtdrop.pack()



    confirmbutton = tk.Button(top, text="Confirm", command=process)
    confirmbutton.grid(column=0, columnspan=2, row=6)

def vehicleReturn():
    def process():
        name = nameentry.get()
        ReturnDate = rtdentry.get()
        vehicleID = vehicleIDentry.get()
        clearAll()

        # Get Customer ID
        query = "SELECT CustID FROM Customer WHERE Name = '{}'".format(name)
        cust = getQuery(query)
        if cust == '':
            queryText.insert(tk.INSERT,"No Customer Found")
            return
        cust = cleaner(cust)
        queryText.insert(tk.INSERT,"Customer ID: " + cust + '\n')
        cust = int(cust)

        query = "SELECT TotalAmount FROM Rental WHERE CustID = {} AND ReturnDate = '{}' AND VehicleID = '{}'".format(cust, ReturnDate, vehicleID)
        total = cleaner(getQuery(query))
        if total == '':
            queryText.insert(tk.INSERT,"No Rental Found")
            return
        queryText.insert(tk.INSERT, "Total Due" + total + "/n")
        query = "UPDATE Rental SET Returned = 1 WHERE CustID = {} AND ReturnDate = '{}' AND VehicleID = '{}'".format(cust, ReturnDate, vehicleID)
        getQuery(query)
        queryText.insert(tk.INSERT, "Vehicle Returned.")
        
        top.destroy()

    top = tk.Toplevel(window)
    top.title("Insert Customer")
    top.geometry("480x480")
    top.resizable(False, False)
    top.configure(background=_color1)

    # TODO: name label/entry, phone label/entry, confirm button
    titlelabel = tk.Label(top, text="Insert Customer info into DB", background=_color1)
    titlelabel.grid(column=0, columnspan=2, row=0)

    namelabel = tk.Label(top, text="Full Name", background=_color1)
    namelabel.grid(column=0, row=1)
    nameentry = tk.Entry(top)
    nameentry.grid(column=1, row=1)

    rtdlabel = tk.Label(top, text="Return Date (YYYY-MM-DD)", background=_color1)
    rtdlabel.grid(column=0, row=2)
    rtdentry = tk.Entry(top)
    rtdentry.grid(column=1, row=2)

    vehicleIDlabel = tk.Label(top, text="vehicleID", background=_color1)
    vehicleIDlabel.grid(column=0, row=3)
    vehicleIDentry = tk.Entry(top)
    vehicleIDentry.grid(column=1, row=3)

    confirmbutton = tk.Button(top, text="Confirm", command=process)
    confirmbutton.grid(column=0, columnspan=2, row=4)

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
editmenu.add_command(label="Insert Vehicle", command=insertVehicle)

menubar.add_cascade(label="Query", menu=querymenu)
menubar.add_cascade(label="Edit", menu=editmenu)

# display window
window.config(menu=menubar)
window.mainloop()
