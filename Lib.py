import mysql.connector

db1 = None

def connect():
    global db1
    db1 = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345"
    )

    c1 = db1.cursor()
    c1.execute("DROP DATABASE IF EXISTS library")
    c1.execute("CREATE DATABASE library")
    c1.execute("USE library")

    c1.execute("CREATE TABLE users (username VARCHAR(30), passw VARCHAR(30))")
    c1.execute("INSERT INTO users VALUES('Ashutosh','12345')")

    c1.execute("CREATE TABLE member (mid VARCHAR(20) PRIMARY KEY, name VARCHAR(50), email VARCHAR(50), phone VARCHAR(20))")
    c1.execute("CREATE TABLE book (bookid VARCHAR(20) PRIMARY KEY, title VARCHAR(50), author VARCHAR(50), publisher VARCHAR(50), cost INTEGER)")
    c1.execute("CREATE TABLE issue (mid VARCHAR(20), bookid VARCHAR(20), dateofissue DATE)")
    c1.execute("CREATE TABLE issuelog (mid VARCHAR(20), bookid VARCHAR(20), dateofissue DATE, dateofreturn DATE)")

    db1.commit()

def login():
    print("-" * 40)
    print("\t Library Management System")
    print("-" * 40)
    print("\t LOGIN")
    un = input("Enter User Name : ")
    pw = input("Enter Password : ")
    q = "SELECT * FROM users WHERE username = %s AND passw = %s"
    val = (un, pw)
    c2 = db1.cursor()
    c2.execute("USE library")
    c2.execute(q, val)
    res = c2.fetchall()
    print("-" * 50)
    if len(res) == 0:
        print("Invalid User Name or Password ")
        print("-" * 50)
        return False
    else:
        print("Access Granted !!!")
        print("-" * 50)
        return True

def addMember():
    print("-" * 50)
    print("\t ADDING A NEW MEMBER")
    print("-" * 50)
    mid = input("Enter Member Id : ")
    name = input("Enter Member Name : ")
    email = input("Enter Email : ")
    phone = input("Enter Phone Number : ")

    cursor1 = db1.cursor()
    q = "INSERT INTO member VALUES (%s,%s,%s,%s)"
    val = (mid, name, email, phone)
    cursor1.execute(q, val)
    db1.commit()
    print("Member Added Successfully")

def delMember():
    print("-" * 40)
    print("\tDELETING A MEMBER")
    print("-" * 40)
    mid = input("Enter Member Id : ")
    cursor1 = db1.cursor()
    q = "DELETE FROM member WHERE mid = %s"
    cursor1.execute(q, (mid,))
    db1.commit()
    print("Member Deleted Successfully")

def showMembers():
    cursor1 = db1.cursor()
    cursor1.execute("SELECT * FROM member")
    res = cursor1.fetchall()
    print("-" * 50)
    print("          MEMBER DETAILS ")
    print("-" * 50)
    print("Id\tName\tEmail\tPhone")
    for k in res:
        print(k[0], "\t", k[1], "\t", k[2], "\t", k[3])
    print("-" * 50)

def addBook():
    print("-" * 50)
    print("\t ADDING A NEW BOOK")
    print("-" * 50)
    bid = input("Enter Book Id : ")
    title = input("Enter Book Title : ")
    author = input("Enter Author name : ")
    pub = input("Enter Publisher :")
    cost = int(input("Enter Cost of the book :"))

    cursor1 = db1.cursor()
    q = "INSERT INTO book VALUES (%s,%s,%s,%s,%s)"
    val = (bid, title, author, pub, cost)
    cursor1.execute(q, val)
    db1.commit()
    print("Book Added Successfully")

def delBook():
    print("-" * 40)
    print("\tDELETING A BOOK")
    print("-" * 40)
    bid = input("Enter Book Id : ")
    cursor1 = db1.cursor()
    q = "DELETE FROM book WHERE bookid = %s"
    cursor1.execute(q, (bid,))
    db1.commit()
    print("Book Deleted Successfully")

def showBooks():
    cursor1 = db1.cursor()
    cursor1.execute("SELECT * FROM book")
    res = cursor1.fetchall()
    print("-" * 50)
    print("          BOOK DETAILS ")
    print("-" * 50)
    print("Id\tTitle\tAuthor\tPublisher\tCost")
    for k in res:
        print(k[0], "\t", k[1], "\t", k[2], "\t", k[3], "\t", k[4])
    print("-" * 50)

def issueBook():
    bid = input("Enter the book id to be issued : ")
    cursor1 = db1.cursor()
    q = "SELECT * FROM issue WHERE bookid = %s"
    cursor1.execute(q, (bid,))
    res = cursor1.fetchall()

    if len(res) == 0:
        mid = input("Enter the member id : ")
        doi = input("Enter the date of issue (YYYY-MM-DD): ")
        q = "INSERT INTO issue (mid, bookid, dateofissue) VALUES (%s, %s, %s)"
        data = (mid, bid, doi)
        cursor1.execute(q, data)
        db1.commit()
        print("-" * 40)
        print(" Book Issued Successfully")
        print("-" * 40)
    else:
        print("-" * 40)
        print("   Sorry! The Book is not available")
        print("-" * 40)

def returnBook():
    bid = input("Enter the book id to be returned : ")
    mid = input("Enter the Member id : ")
    cursor1 = db1.cursor()
    q = "SELECT dateofissue FROM issue WHERE bookid = %s AND mid = %s"
    cursor1.execute(q, (bid, mid))
    res = cursor1.fetchall()

    if len(res) == 0:
        print("-" * 40)
        print("This Book is not Issued to This Member")
        print("-" * 40)
    else:
        dort = input("Enter the date of return (YYYY-MM-DD): ")
        q = "DELETE FROM issue WHERE bookid = %s AND mid = %s"
        cursor1.execute(q, (bid, mid))
        db1.commit()

        q = "INSERT INTO issuelog VALUES (%s, %s, %s, %s)"
        data = (mid, bid, res[0][0], dort)
        cursor1.execute(q, data)
        db1.commit()
        print("Book Returned Successfully")

def showIssued():
    cursor1 = db1.cursor()
    cursor1.execute("SELECT * FROM issue")
    res = cursor1.fetchall()
    print("   LIST OF ISSUED BOOKS   ")
    print("-" * 40)
    print("Member\tBook ID\tIssue Date")
    for k in res:
        print(k[0], "\t", k[1], "\t", k[2])
    print("-" * 40)

def showReturned():
    cursor1 = db1.cursor()
    cursor1.execute("SELECT * FROM issuelog")
    res = cursor1.fetchall()
    print("   LIST OF RETURNED BOOKS   ")
    print("-" * 50)
    print("Member\tBook ID\tIssue Date\tReturn Date")
    for k in res:
        print(k[0], "\t", k[1], "\t", k[2], "\t", k[3])
    print("-" * 50)

# ---- MAIN PROGRAM ----
connect()
print("Connected to database")

if login():
    while True:
        print("-" * 50)
        print("\t CHOOSE AN OPERATION ")
        print("-" * 50)
        print("1. Add a New Member")
        print("2. Delete an Existing Member")
        print("3. Show all Members")
        print("4. Add a New Book")
        print("5. Delete an Existing Book")
        print("6. Show all Books")
        print("7. Issue a Book")
        print("8. Return a Book")
        print("9. Show Issued Books")
        print("10. Show Returned Books")
        print("11. Quit")

        break
