import tkinter as tk    # For GUI Building
from tkinter import messagebox   # For Use Message box
from time import gmtime, strftime  # For Creating Log
import pyttsx3  # For Audio
from threading import Thread   # For Threading

def Voice(message):    # This Function Simply convert Any Text To Message
	engine = pyttsx3.init()
	rate = engine.getProperty('rate')
	engine.setProperty('rate', rate - 90)
	engine.say(message)
	engine.runAndWait()


def is_number(s):    # This Function Simply Check For Value Error
    try:
        float(s)
        return 1
    except ValueError:
        return 0

def check_acc_nmb(num):    #This Function Simply  Check Account Is Exist In Database Or Not
	try:
		fpin=open(num+".txt",'r')
	except FileNotFoundError:
		t = Thread(target=Voice, args=("Invalid Credentials Please Try again",))
		t.start()
		messagebox.showinfo("Error","Invalid Credentials!\nTry Again!")

		return 0
	fpin.close()
	return 

def home_return(master):     # This Function helps to Return To the Main Screen (Windwo)
	master.destroy()
	Main_Menu()

def write(master,name,oc,pin):    # This Logic Make Your account file
	
	if( (is_number(name)) or (is_number(oc)==0) or (is_number(pin)==0)or name==""):
		t = Thread(target=Voice, args=("Invalid Credentials Please Try again",))
		t.start()
		messagebox.showinfo("Error","Invalid Credentials\nPlease try again.")
		master.destroy()
		return 

	f1=open("Accnt_Record.txt",'r')   # This Block of code helps to provide account Number to The new User
	accnt_no=int(f1.readline())
	accnt_no+=1
	f1.close()

	f1=open("Accnt_Record.txt",'w')
	f1.write(str(accnt_no))
	f1.close()

	fdet=open(str(accnt_no)+".txt","w")
	fdet.write(pin+"\n")
	fdet.write(oc+"\n")
	fdet.write(str(accnt_no)+"\n")
	fdet.write(name+"\n")
	fdet.close()

	frec=open(str(accnt_no)+"-rec.txt",'w')
	frec.write("Date                             Credit      Debit     Balance\n")
	frec.write(str(strftime("[%Y-%m-%d] [%H:%M:%S]  ",gmtime()))+"     "+oc+"              "+oc+"\n")  # Its simply Create Log
	frec.close()
	t = Thread(target=Voice, args=(f"Congratulation Your Account Has Been Successfully Opened And Your Account Number Is",))
	t.start()
	messagebox.showinfo("Details","Your Account Number is :- "+str(accnt_no))
	master.destroy()
	return

def crdt_write(master,amt,accnt,name):      # This Function Is use For Update Values of txt file after Credit task complete

	if(is_number(amt)==0):
		t = Thread(target=Voice, args=("Invalid Credentials Please Try again",))
		t.start()
		messagebox.showinfo("Error","Invalid Credentials\nPlease try again.")
		master.destroy()
		return 

	fdet=open(accnt+".txt",'r')
	pin=fdet.readline()
	camt=int(fdet.readline())
	fdet.close()
	amti=int(amt)
	rupee2=int(amt)
	cb=amti+camt
	fdet=open(accnt+".txt",'w')    # Re write all the lines of the file
	fdet.write(pin)
	fdet.write(str(cb)+"\n")
	fdet.write(accnt+"\n")
	fdet.write(name+"\n")
	fdet.close()
	frec=open(str(accnt)+"-rec.txt",'a+')    # This file open for Creating log
	frec.write(str(strftime("[%Y-%m-%d] [%H:%M:%S]  ",gmtime()))+"     "+str(amti)+"              "+str(cb)+"\n")
	frec.close()
	t = Thread(target=Voice, args=(f"Ammount {rupee2} Credited Successfully",))
	t.start()
	messagebox.showinfo("Operation Successfull!!","Amount Credited Successfully!!")
	master.destroy()
	return

def debit_write(master,amt,accnt,name):    # This function update ammount after perform debit task

	if(is_number(amt)==0):   # if user want  to debit 0 ammount then simply give error message
		t = Thread(target=Voice, args=("Invalid Credentials Please Try again",))
		t.start()
		messagebox.showinfo("Error","Invalid Credentials\nPlease try again.")
		master.destroy()
		return 
			
	fdet=open(accnt+".txt",'r')   # Open User File
	pin=fdet.readline()
	camt=int(fdet.readline())
	fdet.close()
	if(int(amt)>camt):    # This print error if user have not enough money which user want to debit
		t = Thread(target=Voice, args=("You dont have that amount left in your account Please try again",))
		t.start()
		messagebox.showinfo("Error!!","You dont have that amount left in your account\nPlease try again.")
	else:
		amti=int(amt)
		rupee=int(amt)
		cb=camt-amti
		fdet=open(accnt+".txt",'w')   # File open and Update values
		fdet.write(pin)
		fdet.write(str(cb)+"\n")
		fdet.write(accnt+"\n")
		fdet.write(name+"\n")
		fdet.close()
		frec=open(str(accnt)+"-rec.txt",'a+')    # File open in a+ mode and its generate log
		frec.write(str(strftime("[%Y-%m-%d] [%H:%M:%S]  ",gmtime()))+"     "+"              "+str(amti)+"              "+str(cb)+"\n")
		frec.close()
		t = Thread(target=Voice, args=(f"Ammount {rupee} Debited Successfully",))
		t.start()
		messagebox.showinfo("Operation Successfull!!","Amount Debited Successfully!!")
		master.destroy()
		return

def Cr_Amt(accnt,name):     # This Function helps To Perform Credit Task
	creditwn=tk.Tk()
	creditwn.geometry("600x300")
	creditwn.title("Credit Amount")
	creditwn.configure(bg="#1E6B7F")
	fr1=tk.Frame(creditwn,bg="blue")
	l_title=tk.Message(creditwn,text="E-CONNECT",relief="raised",width=2000,padx=600,pady=0,fg="black",bg="yellow",justify="center",anchor="center")
	l_title.config(font=("Courier","50","bold"))
	l_title.pack(side="top")
	l1=tk.Label(creditwn,relief="raised",text="Enter Amount to be credited: ")
	e1=tk.Entry(creditwn,relief="raised")   # This Line Get Input From User
	l1.pack(side="top")
	e1.pack(side="top")
	b=tk.Button(creditwn,text="Credit",relief="raised",command=lambda:crdt_write(creditwn,e1.get(),accnt,name))
	b.pack(side="top")     # This Button Helps to Update ammount in the txt file of the user
	creditwn.bind("<Return>",lambda x:crdt_write(creditwn,e1.get(),accnt,name))


def De_Amt(accnt,name):    # This function help for performing Debit task
	debitwn=tk.Tk()   # Creating Object in Class
	debitwn.geometry("600x300")    # Defining window size
	debitwn.title("Debit Amount")	
	debitwn.configure(bg="#1E6B7F")
	fr1=tk.Frame(debitwn,bg="blue")
	l_title=tk.Message(debitwn,text="E-CONNECT",relief="raised",width=2000,padx=600,pady=0,fg="black",bg="yellow",justify="center",anchor="center")
	l_title.config(font=("Courier","50","bold"))
	l_title.pack(side="top")
	l1=tk.Label(debitwn,relief="raised",text="Enter Amount to be debited: ")
	e1=tk.Entry(debitwn,relief="raised")
	l1.pack(side="top")
	e1.pack(side="top")
	b=tk.Button(debitwn,text="Debit",relief="raised",command=lambda:debit_write(debitwn,e1.get(),accnt,name))
	b.pack(side="top")  # This Button helps to Successfully debit ammount and then update value in the txt file
	debitwn.bind("<Return>",lambda x:debit_write(debitwn,e1.get(),accnt,name))   # This Lambda function helps to update value in the user file




def disp_bal(accnt):    # This function is used to Display Balance
	fdet=open(accnt+".txt",'r')  # open txt file of the user
	fdet.readline()
	bal=fdet.readline()   # its simpy jump to the 2nd line which have balance ammount
	fdet.close()
	t = Thread(target=Voice, args=(f"Your Bank Balance is {bal}",))
	t.start()
	messagebox.showinfo("Balance: ",bal)





def disp_tr_hist(accnt):      # This Function help To Display Transaction History
	disp_wn=tk.Tk()
	disp_wn.geometry("900x600")
	disp_wn.title("Transaction History")
	disp_wn.configure(bg="#1E6B7F")
	fr1=tk.Frame(disp_wn,bg="blue")
	l_title=tk.Message(disp_wn,text="E-CONNECT",relief="raised",width=2000,padx=600,pady=0,fg="black",bg="yellow",justify="center",anchor="center")
	l_title.config(font=("Courier","50","bold"))
	l_title.pack(side="top")
	fr1=tk.Frame(disp_wn)
	fr1.pack(side="top")
	l1=tk.Message(disp_wn,text="Your Transaction History:",padx=100,pady=20,width=900,bg="black",fg="white",relief="raised")  # This line Show message
	l1.pack(side="top",pady=10)
	fr2=tk.Frame(disp_wn)
	fr2.pack(side="top")
	frec=open(accnt+"-rec.txt",'r')   # This line open record file of the user
	for line in frec:   # This loop print line one by one
		l=tk.Message(disp_wn,anchor="w",text=line,relief="raised",width=2000)
		l.pack(side="top")
	b=tk.Button(disp_wn,text="Quit",relief="raised",command=disp_wn.destroy)  # This Button helps to quit and return to login window
	b.pack(side="top")
	frec.close()
	t = Thread(target=Voice, args=("Here Is Your Account History",))
	t.start()

def logged_in_menu(accnt,name):   # After Successfully  Login this function show Options To the User
	rootwn=tk.Tk()   # Creating Object In A Class
	rootwn.geometry("1600x500")      # Defining size of window
	rootwn.title("E-CONNECT-"+name)
	rootwn.configure(background='#1E6B7F')  # For Bg Colour
	fr1=tk.Frame(rootwn)
	fr1.pack(side="top")
	l_title=tk.Message(rootwn,text="NET BANKING\n SYSTEM",relief="raised",width=2000,padx=600,pady=0,fg="black",bg="yellow",justify="center",anchor="center")   # For Put Heading In Window
	l_title.config(font=("Courier","50","bold"))
	l_title.pack(side="top")
	label=tk.Label(text="Logged in as:-  "+name,relief="raised",bg="black",fg="white",anchor="center",justify="center") # Its shows name of the person Who Logged In.
	label.pack(side="top")
	img2=tk.PhotoImage(file="credit.gif")     # For Adding Images In window
	myimg2=img2.subsample(2,2)
	img3=tk.PhotoImage(file="debit.gif")
	myimg3=img3.subsample(2,2)
	img4=tk.PhotoImage(file="balance1.gif")
	myimg4=img4.subsample(2,2)
	img5=tk.PhotoImage(file="transaction.gif")
	myimg5=img5.subsample(2,2)
	b2=tk.Button(image=myimg2,command=lambda: Cr_Amt(accnt,name))   # This Button call Credit ammount Function
	b2.image=myimg2
	b3=tk.Button(image=myimg3,command=lambda: De_Amt(accnt,name))  # This Button call Debit ammount Function
	b3.image=myimg3
	b4=tk.Button(image=myimg4,command=lambda: disp_bal(accnt))   # This Button call Display Balance Function
	b4.image=myimg4
	b5=tk.Button(image=myimg5,command=lambda: disp_tr_hist(accnt))  # This Button call Transaction History Function
	b5.image=myimg5
	
	img6=tk.PhotoImage(file="logout.gif")
	myimg6=img6.subsample(2,2)
	b6=tk.Button(image=myimg6,relief="raised",command=lambda: logout(rootwn))    # This Button helps to logout simply by calling logout function
	b6.image=myimg6

	
	b2.place(x=100,y=160)   # Placing Buttons In the Window
	b3.place(x=100,y=230)
	b4.place(x=900,y=160)
	b5.place(x=900,y=230)
	b6.place(x=500,y=400)
	t = Thread(target=Voice, args=(f"Welcome Back {name}",))
	t.start()
	
def logout(master):    # This function helps to logout to the login page and return to the main window
	t = Thread(target=Voice, args=("You Have Been Successfully Logged Out",))
	t.start()
	messagebox.showinfo("Logged Out","You Have Been Successfully Logged Out!!")
	master.destroy()
	Main_Menu()


def check_log_in(master,name,acc_num,pin):
	if(check_acc_nmb(acc_num)==0):
		master.destroy()
		Main_Menu()
		return

	if( (is_number(name))  or (is_number(pin)==0) ):
		messagebox.showinfo("Error","Invalid Credentials\nPlease try again.")
		t = Thread(target=Voice, args=("Invalid Credentials Please Try again",))
		t.start()

		master.destroy()
		Main_Menu()
	else:
		master.destroy()
		logged_in_menu(acc_num,name)

global name
def log_in(master):    # Login Function Which helps to Show Login Window
	master.destroy()   # This Line Simply Erase root Window
	loginwn=tk.Tk()					# Create Object in Tk() Class
	loginwn.geometry("600x350") # Defining Size of Window
	loginwn.title("Log in")
	loginwn.configure(bg="#1E6B7F")
	l_title=tk.Message(loginwn,text="E-CONNECT",relief="raised",width=2000,padx=600,pady=0,fg="black",bg="yellow",justify="center",anchor="center")  # Show Message of the Window
	l_title.config(font=("Courier","50","bold"))
	l_title.pack(side="top",pady=5)
	l1=tk.Label(loginwn,text="Enter Name:",relief="raised")    # Its Show text to user For get Input By User
	l1.pack(side="top",pady=5)
	e1=tk.Entry(loginwn)     # Entry Box get input by the user
	name=e1.get()
	e1.pack(side="top")
	l2=tk.Label(loginwn,text="Enter account number:",relief="raised")
	l2.pack(side="top",pady=5)
	e2=tk.Entry(loginwn)
	e2.pack(side="top")
	l3=tk.Label(loginwn,text="Enter your PIN:",relief="raised")
	l3.pack(side="top",pady=5)
	e3=tk.Entry(loginwn,show="*")
	e3.pack(side="top")
	b=tk.Button(loginwn,text="Submit",command=lambda: check_log_in(loginwn,e1.get().strip(),e2.get().strip(),e3.get().strip()))    # This Function call the check_log_in funtion and five arguments which is get by user
	b.pack(side="top",pady=5)
	b1=tk.Button(text="HOME",relief="raised",bg="black",fg="white",command=lambda: home_return(loginwn))
	b1.pack(side="top")   # This button return to the main window
	loginwn.bind("<Return>",lambda x:check_log_in(loginwn,e1.get().strip(),e2.get().strip(),e3.get().strip()))
	t = Thread(target=Voice, args=("Enter Your Login Details",))
	t.start()

def Create():  # Create New Account Function
	crwn=tk.Tk()           # Create Another Object For Making Create New Account Window
	crwn.geometry("600x320")   # Defining Window Size of the Window
	crwn.title("Create Account")
	crwn.configure(bg="#1E6B7F")     # For Adding Background color
	l_title=tk.Message(crwn,text="E-CONNECT",relief="raised",width=1800,padx=600,pady=0,fg="black",bg="yellow",justify="center",anchor="center")
	l_title.config(font=("Courier","50","bold"))
	l_title.pack(side="top",pady=5)
	l1=tk.Label(crwn,text="Enter Name:",relief="raised")  # This Helps to Get A Values By user
	l1.pack(side="top",pady=5)
	e1=tk.Entry(crwn)   # And user Put Entry In this Entry Box
	e1.pack(side="top")
	l2=tk.Label(crwn,text="Enter opening credit:",relief="raised")
	l2.pack(side="top",pady=5)
	e2=tk.Entry(crwn)
	e2.pack(side="top")
	l3=tk.Label(crwn,text="Enter desired PIN:",relief="raised")
	l3.pack(side="top",pady=5)
	e3=tk.Entry(crwn,show="*")    # This Line Helps to get a Password Type Input From user
	e3.pack(side="top")
	b=tk.Button(crwn,text="Submit",command=lambda: write(crwn,e1.get().strip(),e2.get().strip(),e3.get().strip())) # This Line Easily take input from the user and remove all spaces and get input by using .get() Functionn
	b.pack(side="top",pady=5)
	crwn.bind("<Return>",lambda x:write(crwn,e1.get().strip(),e2.get().strip(),e3.get().strip()))  # This Line Deal With Event for a widget
	t = Thread(target=Voice, args=("Please Enter Your Details",))
	t.start()

	return


def Main_Menu():   # Main function which handle all the program
	rootwn=tk.Tk()   # Creating an Object
	rootwn.geometry("1600x500")       # Define Size of default Window Size
	rootwn.title("E - CONNECT")   # Title of Main Program Window
	fr1=tk.Frame(rootwn)
	fr1.pack(side="top")
	bg_image = tk.PhotoImage(file ="mainimage.png")   # For add background Image of the Main Window
	x = tk.Label (image = bg_image)
	x.place(y=-400)
	l_title=tk.Message(text="NET BANKING\nSYSTEM",relief="raised",width=2000,padx=600,pady=0,fg="black",bg="yellow",justify="center",anchor="center")  # For Adding Heading
	l_title.config(font=("Courier","50","bold"))
	l_title.pack(side="top")
	imgc1=tk.PhotoImage(file="Create New.png")    # Create New Account Image Use as Button
	imglo=tk.PhotoImage(file="login.gif")
	imgc=imgc1.subsample(2,2)
	imgc=imgc1.subsample(2,2)
	imglog=imglo.subsample(2,2)
	b1=tk.Button(image=imgc,command=Create)   # Its refers to create new account function
	b1.image=imgc   # Its convert Image to Button
	b2=tk.Button(image=imglog,command=lambda: log_in(rootwn))  # Its refers to login account function using Lambda Function
	b2.image=imglog
	img6=tk.PhotoImage(file="quit.png")
	myimg6=img6.subsample(2,2)

	b6=tk.Button(image=myimg6,command=rootwn.destroy)     # This Button Simply Close Program Using Destroy Property
	b6.image=myimg6
	b1.place(x=800,y=300)    # Place Button In Window Using Place Method
	b2.place(x=800,y=200)	
	b6.place(x=920,y=400)
	t = Thread(target=Voice, args=("Welcome To E Connect",))
	t.start()
	rootwn.mainloop() # its Hepls To Perform All Functions or All Logic Inside the rootwn Object Which is Use Tkinter Class

Main_Menu()    # Calling The Main Function

# Thanks for Using
# Made By Piyush Trivedi