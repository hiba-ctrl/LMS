

#set FLASK_APP=Library_system\app.py
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request

# create the application object
app = Flask(__name__)


import pymongo

#myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mongopassword = "QrMM8ElNzeMHytwo"

myclient = pymongo.MongoClient('mongodb+srv://hiba:'+ mongopassword +'@cluster0.1g2q2.mongodb.net/?retryWrites=true&w=majority')


mydb = myclient.Library

memebersCol = mydb["Members"]
AdminsCol = mydb["Admins"]
booksCol = mydb["Books"]
borrowersCol = mydb["Borrowers"]
suppliersCol = mydb["Suppliers"]

'''
# use decorators to link the function to a url
@app.route('/home')
def home(user):
    return render_template('indexwrite.html', user= user)  # render a template
'''


#<!-- tr:hover {background-color: #D6EEEE;} -->
# Route for handling the login page logic
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    global username
    global password


    if request.method == 'POST':

        type= ""
        try :
            y = AdminsCol.find_one({"username": request.form['username'], "admin_id" : int(request.form['password'])})



            print ( y)
            print ( request.form['username'] ,request.form['password'] )
            if ( y is None) :


                try :
                    print ("here")
                    y = memebersCol.find_one({"firstName": request.form['username'], "memberId": int(request.form['password'])})
                    print ( y)
                    if (y is None):
                        error = '❌ Invalid Credentials. Please try again.'

                    else :


                        username = request.form['username'].upper()
                        password = int(request.form['password'])

                        submission_successful = True  # or False. you can determine this.
                        # return render_template("confirm.html",  submission_successful=submission_successful),{"Refresh": "3; url=/AdminHome"}
                        message = "✔ You are Now Logged In !"
                        return render_template("confirmLogin.html", user=username,
                                               submission_successful=submission_successful, message=message), {"Refresh": "1; url=/MemberHome"}


                except Exception as e  :
                    error = '❌ Invalid Credentials. Please try again.'

            else :

                username = request.form['username'].upper()
                password = int(request.form['password'])

                submission_successful = True  # or False. you can determine this.
                # return render_template("confirm.html",  submission_successful=submission_successful),{"Refresh": "3; url=/AdminHome"}
                message = "✔ You are Now Logged In !"
                return render_template("confirmLogin.html", user=username,
                                       submission_successful=submission_successful, message=message), {"Refresh": "1; url=/AdminHome"}


        except Exception as e:

            error = '❌ Invalid Credentials. Please try again.'


    return render_template('login.html', error=error)

@app.route('/logout', methods=['GET', 'POST'])
def logout() :
    return redirect("/")


@app.route('/MemberHome', methods=['GET', 'POST'])
def MemberHome() :



    currentDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    currentDate = datetime.strptime(currentDate, '%Y-%m-%d %H:%M:%S')


    borrwDetails = borrowersCol.find()


    for x in borrwDetails :

        DueDate = x["DueDate"]


        if (currentDate> DueDate ):


            late_days = (currentDate - DueDate)

            LateFine = float(int(late_days.days) * 10)

            query = {'BookID': int(x["BookID"]) , 'MemberID' : int(x['MemberID'])}
            val = {"$set": {'LateFine': LateFine}}

            borrowersCol.update_one(query, val)




    print("ok")
    type = "Member"


    try :


        memberId = memebersCol.find_one({'memberId': password})
        memberId = memberId['memberId']

    except :

        memberId = memebersCol.find_one({'firstName': username})
        memberId = memberId['memberId']


    books = booksCol.find()
    reserved = borrowersCol.find({"MemberID": memberId })




    return render_template('indexwriteMember.html',memberId=memberId,  user=username, books=books, reserved=reserved
                           )  # render a template



@app.route('/AdminHome', methods=['GET', 'POST'])
def AdminHome() :




    currentDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    currentDate = datetime.strptime(currentDate, '%Y-%m-%d %H:%M:%S')


    borrwDetails = borrowersCol.find()


    for x in borrwDetails :

        DueDate = x["DueDate"]


        if (currentDate> DueDate ):


            late_days = (currentDate - DueDate)

            LateFine = float(int(late_days.days) * 10)

            query = {'BookID': int(x["BookID"]) , 'MemberID' : int(x['MemberID'])}
            val = {"$set": {'LateFine': LateFine}}

            borrowersCol.update_one(query, val)



    type = "Admin"


    books = booksCol.find()
    members = memebersCol.find()
    borrowers = borrowersCol.find()
    suppliers = suppliersCol.find()
    return render_template('indexwrite.html', user=username, books=books, members=members,
                           borrowers=borrowers, suppliers = suppliers)  # render a template






@app.route('/deleteBook', methods=['GET', 'POST'])
def deleteBook() :


    bookId = request.form['delB']

    print (bookId)

    booksCol.delete_one({'BookID':int(bookId) })

    submission_successful = True  # or False. you can determine this.
    # return render_template("confirm.html",  submission_successful=submission_successful),{"Refresh": "3; url=/AdminHome"}
    message = "✔ Book deleted Succesfully !"
    return render_template("confirm.html", user=username, submission_successful=submission_successful, message=message)


@app.route('/editBook', methods=['GET', 'POST'])
def editBook() :


    bookId = request.form['editB']
    print ( bookId)
    #returning the information of the book to be edited
    book = booksCol.find_one({'BookID': int (bookId )})
    #using flask to show a new html page
    return render_template('editBook.html', user=username, book = book)  # render a template



@app.route('/UpdateBook', methods=['GET', 'POST'])
def UpdateBook() :
    #MongoDB crud
    bookId = int(request.form['BookID'])
    #this gets all the information of the book from mongodb
    book = booksCol.find_one({'BookID': int(bookId)})


    try :
        #request.form is for recovering information from the form
        title = request.form['Title']
        Author = request.form['Author']
        Availability = request.form['Availability']
        Price = float(request.form['Price'])
        PublisherAddress = request.form['PublisherAddress']
        PublisherName = request.form['PublisherName']
        PublisherPhone = request.form['PublisherPhone']

        #booksCol.find_one({'BookID': int(bookId)})
        #query specify which book where are going to edit using bookID
        query = {"BookID": bookId}
        #val will define all the edited infos in the forms
        val = {"$set": { 'Title' :  title, 'Author' : Author , 'Availability' : Availability ,
                        'Price' : Price, 'PublisherAddress' :PublisherAddress, 'PublisherName' :PublisherName , 'PublisherPhone':  PublisherPhone   }}
        #we choose Book collection and pass the query and vals to update in our db
        booksCol.update_many(query, val)

        submission_successful = True  # or False. you can determine this.
        #return render_template("confirm.html",  submission_successful=submission_successful),{"Refresh": "3; url=/AdminHome"}
        message = "✔ Book Updated Succesfully !"
        return render_template("confirm.html", user=username,submission_successful=submission_successful,message=message)


    except :


        error = '❌ Invalid parameters ! Please try again.'
        #render same template of editBook to give the chance to the user to try again
        return render_template('editBook.html', user=username, book=book, error=error)  # render a template






@app.route('/CancelOperation', methods=['GET', 'POST'])
def CancelOperation() :


    return redirect("/AdminHome")




@app.route('/CancelOperationMember', methods=['GET', 'POST'])
def CancelOperationMember() :


    return redirect("/MemberHome")



@app.route('/add_book', methods=['GET', 'POST'])
def add_book() :


    return render_template('addBook.html', user=username)  # render a template



@app.route('/InsertBook', methods=['GET', 'POST'])
def InsertBook() :

    try :
     bookId = int(request.form['BookID'])
    except :

        error = '❌ Book ID should an unique integer ! Please try again.'
        return render_template('addBook.html', user=username,  error=error)  # render a template

    book = booksCol.find_one({'BookID': int(bookId)})

    if ( book == None) :

        try:

            title = request.form['Title']
            Author = request.form['Author']
            Availability = request.form['Availability']
            Price = float(request.form['Price'])
            PublisherAddress = request.form['PublisherAddress']
            PublisherName = request.form['PublisherName']
            PublisherPhone = request.form['PublisherPhone']


            mongodict=  {"BookID" : bookId,  'Title': title, 'Author': Author, 'Availability': Availability,
                            'Price': Price, 'PublisherAddress': PublisherAddress, 'PublisherName': PublisherName,
                            'PublisherPhone': PublisherPhone}

            booksCol.insert_one(mongodict)



            submission_successful = True  # or False. you can determine this.
            # return render_template("confirm.html",  submission_successful=submission_successful),{"Refresh": "3; url=/AdminHome"}
            message = "✔ Book Inserted Succesfully !"
            return render_template("confirm.html",user=username, submission_successful=submission_successful,message=message)

        except:

            error = '❌ Invalid parameters ! Please try again.'
            return render_template('addBook.html', user=username, book=book, error=error)  # render a template

    else :

        error = '❌ Duplicated entry ! Please try again.'
        return render_template('addBook.html', user=username, book=book, error=error)  # render a template





@app.route('/editMember', methods=['GET', 'POST'])
def editMember() :


    memberId = request.form['editM']
    print ( memberId)

    member = memebersCol.find_one({'memberId': int (memberId )})

    return render_template('editMember.html', user=username, member = member)  # render a template




@app.route('/UpdateMember', methods=['GET', 'POST'])
def UpdateMember() :

    memberId = int(request.form['memberId'])
    member = memebersCol.find_one({'memberId': int(memberId)})


    try :

        firstName = request.form['firstName']
        lastName = request.form['lastName']
        address = request.form['address']
        phone = request.form['phone']

        membershipDate = request.form['membershipDate']


        membershipDate = datetime.strptime(membershipDate, '%Y-%m-%d %H:%M:%S')

        expiryDate = request.form['expiryDate']
        expiryDate = datetime.strptime(expiryDate, '%Y-%m-%d %H:%M:%S')

        memebersCol.find_one({'memberId': int(memberId)})

        query = {"memberId": memberId}
        val = {"$set": { 'firstName' :  firstName, 'lastName' : lastName , 'address' : address ,
                        'phone' : phone, 'membershipDate' :membershipDate, 'expiryDate' :expiryDate    }}

        memebersCol.update_many(query, val)

        submission_successful = True  # or False. you can determine this.
        #return render_template("confirm.html",  submission_successful=submission_successful),{"Refresh": "3; url=/AdminHome"}
        message = "✔ Member details Updated Succesfully !"
        return render_template("confirm.html",user=username, submission_successful=submission_successful,message=message)


    except Exception as e :


        error = '❌ Invalid parameters ! Please try again.'

        return render_template('editMember.html', user=username, member=member, error=error)  # render a template




@app.route('/deleteMember', methods=['GET', 'POST'])
def deleteMember() :


    memberId = request.form['delM']

    print (memberId)

    memebersCol.delete_one({'memberId':int(memberId) })

    submission_successful = True  # or False. you can determine this.
    # return render_template("confirm.html",  submission_successful=submission_successful),{"Refresh": "3; url=/AdminHome"}
    message = "✔ Member deleted Succesfully !"
    return render_template("confirm.html", user=username, submission_successful=submission_successful, message=message)








@app.route('/add_member', methods=['GET', 'POST'])
def add_member() :


    return render_template('addMember.html', user=username)  # render a template






@app.route('/InsertMember', methods=['GET', 'POST'])
def InsertMember() :

    try :
     memberId = int(request.form['memberId'])
    except :

        error = '❌ Member ID should an unique integer ! Please try again.'
        return render_template('addMember.html', user=username,  error=error)  # render a template

    member = memebersCol.find_one({'memberId': int(memberId)})

    if ( member == None) :

        try:

            firstName = request.form['firstName']
            lastName = request.form['lastName']
            address = request.form['address']
            phone = request.form['phone']

            membershipDate = request.form['membershipDate'].replace('T',' ')

            membershipDate = datetime.strptime(membershipDate, '%Y-%m-%d %H:%M:%S')

            expiryDate = request.form['expiryDate'].replace('T',' ')
            expiryDate = datetime.strptime(expiryDate, '%Y-%m-%d %H:%M:%S')




            mongodict=  {"memberId" : memberId,  'firstName': firstName, 'lastName': lastName, 'address': address,
                            'phone': phone, 'membershipDate': membershipDate, 'expiryDate': expiryDate
                       }

            memebersCol.insert_one(mongodict)



            submission_successful = True  # or False. you can determine this.
            # return render_template("confirm.html",  submission_successful=submission_successful),{"Refresh": "3; url=/AdminHome"}
            message = "✔ New Member Inserted Succesfully !"
            return render_template("confirm.html",user=username, submission_successful=submission_successful,message=message)

        except Exception as e:


            error = '❌ Invalid parameters ! Please try again.'
            return render_template('addMember.html', user=username, member=member, error=error)  # render a template

    else :

        error = '❌ Duplicated entry ! Please try again.'
        return render_template('addMember.html', user=username, member=member, error=error)  # render a template




@app.route('/extendDate', methods=['GET', 'POST'])
def extendDate() :


    BookID =  int(request.form['BookID'])
    memberId = int(request.form['memberId'])

    return render_template('extendDate.html', user=username, BookID=BookID, memberId=memberId)  # render a template



@app.route('/updateDueDate', methods=['GET', 'POST'])
def updateDueDate() :

    BookID =  int(request.form['BookID'])
    memberId = int(request.form['memberId'])

    try :

        DueDate = request.form['DueDate'].replace('T',' ')

        DueDate = datetime.strptime(DueDate, '%Y-%m-%d %H:%M:%S')

    except  Exception as e:

        error = '❌ Invalid Date ! Please try again.'

        return render_template('extendDate.html', user=username, BookID=BookID, memberId=memberId,
                               error=error)  # render a template

    CurrentDate = borrowersCol.find_one({'BookID': BookID, 'MemberID' : memberId })

    details = borrowersCol.find_one({'BookID': BookID, 'MemberID': memberId})

    CurrentDate = CurrentDate['DueDate']

    #CurrentDate = datetime.strptime(CurrentDate, '%Y-%m-%d %H:%M:%S')

    print ( "current", CurrentDate)


    Extensions = int ( details['DueDate_Extensions'])


    if ( CurrentDate <= DueDate ) :

        Extensions+=1
        query = {"MemberID": int(memberId), 'BookID': int(BookID) }
        val = {"$set": {'DueDate': DueDate,  'DueDate_Extensions' : Extensions }}

        borrowersCol.update_many(query, val)

        submission_successful = True  # or False. you can determine this.
        # return render_template("confirm.html",  submission_successful=submission_successful),{"Refresh": "3; url=/AdminHome"}
        message = "✔ Due date extended Succesfully !"
        return render_template("confirm.html",user=username, submission_successful=submission_successful, message=message)

    else :

        error = '❌ Invalid Date ! Please select a date higher than the current one.'

        return render_template('extendDate.html', user=username,BookID=BookID, memberId=memberId, error=error)  # render a template







@app.route('/add_borrower', methods=['GET', 'POST'])
def add_borrower() :


    members = memebersCol.find()
    books = booksCol.find({'Availability' : { '$in' : ["Yes","yes","YES"]}})

    return render_template('addBorrower.html', user=username, books=books, members=members)  # render a template



@app.route('/InsertBorrower', methods=['GET', 'POST'])
def InsertBorrower() :


    try:
        bookId = int(request.form['books'])
        memberId =int(request.form['members'])


        DueDate = request.form['DueDate'].replace('T', ' ')

        DueDate = datetime.strptime(DueDate, '%Y-%m-%d %H:%M:%S')

        returnDate = None
        LateFine= 0.0



        print ( bookId)

        print ( memberId)

        mongodict=  {"BookID" : int(bookId),  'MemberID': int(memberId), 'ReturnDate': returnDate, 'DueDate':DueDate, 'LateFine': float(LateFine), 'DueDate_Extensions' : 0   }

        borrowersCol.insert_one(mongodict)

        query = {'BookID': int(bookId) }
        val = {"$set": {'Availability': 'No'}}

        booksCol.update_many(query, val)





        submission_successful = True  # or False. you can determine this.
        # return render_template("confirm.html",  submission_successful=submission_successful),{"Refresh": "3; url=/AdminHome"}
        message = "✔ Borrower added Succesfully !"
        return render_template("confirm.html",user=username, submission_successful=submission_successful,message=message)

    except:

            error = '❌ Invalid parameters ! Please try again.'
            members = memebersCol.find()
            books = booksCol.find({'Availability': {'$in': ["Yes", "yes", "YES"]}})

            return render_template('addBorrower.html', error=error, user=username, books=books, members=members)  # render a template






@app.route('/ReturnBook', methods=['GET', 'POST'])
def ReturnBook() :


    MemberID = int(request.form['MemberID'])


    bookId = int(request.form['BookID'])
    book = booksCol.find_one({'BookID' : int(bookId) })

    returnDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    returnDate = datetime.strptime(returnDate, '%Y-%m-%d %H:%M:%S')


    DueDate = request.form['DueDate']

    DueDate = datetime.strptime(DueDate, '%Y-%m-%d %H:%M:%S')

    #LateFine= int(request.form['LateFine'])



    if ( returnDate <= DueDate) :

        LateFine= 0.0

    else:

        late_days =  (returnDate - DueDate)

        LateFine = float ( int ( late_days.days) * 10 )


    return render_template('ReturnBook.html', user=username,MemberID=MemberID, book=book, ReturnDate =returnDate , DueDate = DueDate, LateFine=LateFine  )  # render a template




@app.route('/ReleaseBook', methods=['GET', 'POST'])
def ReleaseBook() :

    try :

        MemberID = int(request.form['MemberID'])

        bookId = int(request.form['BookID'])

        book = booksCol.find_one({'BookID': bookId})

        returnDate = request.form['ReturnDate']

        returnDate = datetime.strptime(returnDate, '%Y-%m-%d %H:%M:%S')

        DueDate = request.form['DueDate']

        DueDate = datetime.strptime(DueDate, '%Y-%m-%d %H:%M:%S')

        LateFine = float(request.form['LateFine'])
    except :

        submission_successful = True
        message = '❌ Invalid Database Entry! Please try again.'

        return render_template("confirmMember.html", user=username, submission_successful=submission_successful,
                               message=message)


    try :

        query = {'BookID': int(bookId), "MemberID" : int(MemberID)}
        val = {"$set": {'ReturnDate': returnDate,  'LateFine': float(LateFine) }}

        borrowersCol.update_many(query, val)


        query = {'BookID': int(bookId)}
        val = {"$set": {'Availability': "Yes"}}

        booksCol.update_many(query, val)

        submission_successful = True  # or False. you can determine this.
        # return render_template("confirm.html",  submission_successful=submission_successful),{"Refresh": "3; url=/AdminHome"}
        message = "✔ Book returned to library Succesfully !"
        return render_template("confirmMember.html", user=username, submission_successful=submission_successful,
                               message=message)


    except :

        error = '❌ Invalid parameters ! Please try again.'

        return render_template('ReturnBook.html', user=username, MemberID=MemberID, book=book, returnDate=returnDate,
                               DueDate=DueDate, LateFine=LateFine)  # render a template






@app.route('/BorrowBook', methods=['GET', 'POST'])
def BorrowBook() :

    bookId = int(request.form['BookID'])

    bookName =request.form['Title']

    memberId = int(request.form['memberId'])

    DueDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    DueDate = datetime.strptime(DueDate, '%Y-%m-%d %H:%M:%S')

    DueDate = DueDate + relativedelta(months=1)


    return render_template('BorrowBook.html', user=username, memberId= memberId, DueDate=DueDate, bookId=bookId, bookName=bookName)  # render a template


@app.route('/MemberBorrow', methods=['GET', 'POST'])
def MemberBorrow() :


    try :

        bookId = int(request.form['BookID'])

        bookName = request.form['Title']

        memberId = int(request.form['memberId'])

        DueDate = request.form['DueDate']

        DueDate = datetime.strptime(DueDate, '%Y-%m-%d %H:%M:%S')

        returnDate = None

        LateFine = 0.0


        mongodict=  {"BookID" : int(bookId),  'MemberID': int(memberId), 'ReturnDate': returnDate, 'DueDate':DueDate, 'LateFine': float(LateFine), 'DueDate_Extensions': 0    }

        borrowersCol.insert_one(mongodict)

        query = {'BookID': int(bookId) }
        val = {"$set": {'Availability': 'No'}}

        booksCol.update_many(query, val)


        submission_successful = True  # or False. you can determine this.
        # return render_template("confirm.html",  submission_successful=submission_successful),{"Refresh": "3; url=/AdminHome"}
        message = "✔ Book Borrowed Succesfully ! "
        return render_template("confirmMember.html",user=username, submission_successful=submission_successful,message=message)


    except Exception as e :



            error = '❌ Invalid parameters ! Please try again.'


            return render_template('BorrowBook.html', user=username, memberId=memberId, DueDate=DueDate, bookId=bookId,bookName=bookName,error=error)  # render a template





@app.route('/add_supplier', methods=['GET', 'POST'])
def add_supplier() :


    return render_template('addSupplier.html', user=username)  # render a template






@app.route('/InsertSupplier', methods=['GET', 'POST'])
def InsertSupplier() :

    try :
     supplierID = int(request.form['supplierID'])
    except :

        error = '❌ Supplier ID should an unique integer ! Please try again.'
        return render_template('addSupplier.html', user=username,  error=error)  # render a template

    supplier = suppliersCol.find_one({'supplierID': int(supplierID)})

    if ( supplier == None) :

        try:

            firstName = request.form['firstName']
            lastName = request.form['lastName']
            address = request.form['address']
            phone = request.form['phone']
            booksSupplied = request.form['booksSupplied']


            mongodict=  {"supplierID" : supplierID,  'firstName': firstName, 'lastName': lastName, 'address': address,
                            'phone': phone, 'booksSupplied'  : booksSupplied
                       }

            suppliersCol.insert_one(mongodict)



            submission_successful = True  # or False. you can determine this.
            # return render_template("confirm.html",  submission_successful=submission_successful),{"Refresh": "3; url=/AdminHome"}
            message = "✔ New Supplier Inserted Succesfully !"
            return render_template("confirm.html",user=username, submission_successful=submission_successful,message=message)

        except Exception as e:


            error = '❌ Invalid parameters ! Please try again.'
            return render_template('addMember.html', user=username, member=supplier, error=error)  # render a template

    else :

        error = '❌ Duplicated entry ! Please try again.'
        return render_template('addSupplier.html', user=username, supplier=supplier, error=error)  # render a template



















@app.route('/member_sign', methods=['GET', 'POST'])
def member_sign() :


    return render_template('addMemberSignup.html')  # render a template




@app.route('/InsertMemberSignUp', methods=['GET', 'POST'])
def InsertMemberSignUp() :

    try :
     memberId = int(request.form['memberId'])
    except :

        error = '❌ Member ID should an unique integer ! Please try again.'
        return render_template('addMemberSignup.html',   error=error)  # render a template

    member = memebersCol.find_one({'memberId': int(memberId)})

    if ( member == None) :

        try:

            firstName = request.form['firstName']
            lastName = request.form['lastName']
            address = request.form['address']
            phone = request.form['phone']

            membershipDate = request.form['membershipDate'].replace('T',' ')

            membershipDate = datetime.strptime(membershipDate, '%Y-%m-%d %H:%M:%S')

            expiryDate = request.form['expiryDate'].replace('T',' ')
            expiryDate = datetime.strptime(expiryDate, '%Y-%m-%d %H:%M:%S')




            mongodict=  {"memberId" : memberId,  'firstName': firstName, 'lastName': lastName, 'address': address,
                            'phone': phone, 'membershipDate': membershipDate, 'expiryDate': expiryDate
                       }

            memebersCol.insert_one(mongodict)



            submission_successful = True  # or False. you can determine this.
            # return render_template("confirm.html",  submission_successful=submission_successful),{"Refresh": "3; url=/AdminHome"}
            message = "✔ New Member Inserted Succesfully !"
            return render_template("confirmMemberSignup.html", submission_successful=submission_successful,message=message)

        except Exception as e:

            raise e
            error = '❌ Invalid parameters ! Please try again.'
            return render_template('addMemberSignup.html',  member=member, error=error)  # render a template

    else :

        error = '❌ Duplicated entry ! Please try again.'
        return render_template('addMemberSignup.html', member=member, error=error)  # render a template



# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)