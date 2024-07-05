# Modules
from tkinter import *
from PIL import Image,ImageTk
from MenuFunctions import *
from Buttons import button_definitions
from tkinter import messagebox as tmsg
import os
import tempfile
import mysql.connector as mysql

# Function
def welcome():
    receiptArea.delete(1.0,END)
    receiptArea.insert(END,"\t Indian Institute of Technology and Mnagement")
    pic = Image.open("Images\\ISTE.png")
    resized_pic = pic.resize((58,65), Image.ANTIALIAS)
    global image
    image = ImageTk.PhotoImage(resized_pic)
    receiptArea.insert(END,"\t\t\t\t\t\t\t")
    receiptArea.insert(END,"\n\t____________________________________________\t\t\t\t")
    receiptArea.image_create(END,image=image)
    receiptArea.insert(END,"\nName :")
    receiptArea.insert(END,"\nDesignation :")
    receiptArea.insert(END,"\nPayscale :")

def reset():
    Entry_variables.Employee_id.set("")
    Entry_variables.Employee_name.set("")
    No_of_days.set("select")
    leave.set("0") 
    Entry_variables.Basic_pay.set("0")
    Entry_variables.Grade_pay.set("0")
    Entry_variables.CEA.set("0")
    Entry_variables.Others.set("0")
    Entry_variables.total_deduction.set("0")
    Entry_variables.income_tax.set("0")
    Entry_variables.CPF_amount.set("0")
    Entry_variables.festive_amount.set("0")  
    instalment1.set("Instl")
    instalment2.set("Instl")
    welcome()


def generate_receipt():
    if(Entry_variables.Employee_id.get() != "" and int(Entry_variables.Employee_id.get())<9 and int(Entry_variables.Employee_id.get())>=0):
        # GrossPay
        day30 = ["April", "June","September", "November"]
        if(No_of_days.get() in day30):
            N_o_d = 30
        elif(No_of_days.get()=="February"):
            N_o_d = 28
        else:
            N_o_d = 31
        effective_days = N_o_d - int(leave.get())
        BasicPay = (Entry_variables.Basic_pay.get()/N_o_d)*effective_days
        GradePay = (Entry_variables.Grade_pay.get()/N_o_d)*effective_days
        HandA = 0.3*(BasicPay+GradePay)
        DA = 2.03*(BasicPay+GradePay)
        TA = (3200/N_o_d)*effective_days
        DAonTA = 2.03* TA
        CEA = (Entry_variables.CEA.get()/N_o_d)*effective_days
        others = (Entry_variables.Others.get()/N_o_d)*effective_days
        GrossPay = BasicPay + GradePay + HandA + DA + TA + DAonTA + Entry_variables.CEA.get() + Entry_variables.Others.get()

        # Deductions
        CPF = 0.2 * (BasicPay + GradePay)
        VPF = Entry_variables.total_deduction.get() - CPF
        if(Entry_variables.CPF_amount.get()==0):
            CPFAdvance = 0
        elif(instalment1.get()=="Instl"):
            tmsg.showerror("showerror", "CPF Advance Installment not selected")
        else:
            CPFAdvance = Entry_variables.CPF_amount.get()/int(instalment1.get())

        if(Entry_variables.festive_amount.get()==0):
            FestiveAdvance = 0
        elif(instalment2.get()=="Instl"):
            tmsg.showerror("showerror", "Festive Advance Installment not selected")
        else:
            FestiveAdvance = Entry_variables.festive_amount.get()/int(instalment2.get())

        TotalDeduction = Entry_variables.total_deduction.get() + CPFAdvance + FestiveAdvance + Entry_variables.income_tax.get()

        # NetPay
        NetPay = "%.2f"%(GrossPay - TotalDeduction)
        # print(NetPay)

        # Adding to the Textbox
        receiptArea.insert(3.7,f"\t\t{Entry_variables.Employee_name.get()}({Entry_variables.Employee_id.get()})")
        receiptArea.insert(4.14,f"\t\t{data[3]}")
        receiptArea.insert(5.11,f"\t\t{data[2]}")
        receiptArea.insert(END,f"\n\t\t===============================")
        receiptArea.insert(END,f"\nMonth : {No_of_days.get()}\t\t\t\t\tDEDUCTIONS")
        receiptArea.insert(END,f"\n\nUnauthorized Leaves Taken : {leave.get()}\t\t\t\t\tCPF : {CPF}")
        receiptArea.insert(END,f"\nBasic Pay : {BasicPay}\t\t\t\t\tVPF : {VPF}")
        receiptArea.insert(END,f"\nGrade Pay : {GradePay}\t\t\t\t\tCPF Advance : {CPFAdvance}")
        receiptArea.insert(END,f"\nH and A : {HandA}\t\t\t\t\tFestive Advance : {FestiveAdvance}")
        receiptArea.insert(END,f"\nDA : {DA}\t\t\t\t\tIncome Tax : {Entry_variables.income_tax.get()}")
        receiptArea.insert(END,f"\nTA : {TA}")
        receiptArea.insert(END,f"\nDA on TA : {DAonTA}")
        receiptArea.insert(END,f"\nCEA : {CEA}")
        receiptArea.insert(END,f"\nOthers : {others}")
        receiptArea.insert(END,f"\nGross Pay : {GrossPay}\t\t\t\t\tTotal Deductions : {TotalDeduction}")
        receiptArea.insert(END,f"\n_________________________________________________________________")
        receiptArea.insert(END,f"\n\n\tNet Pay : {NetPay}")
        receiptArea.insert(END,f"\n_________________________________________________________________")
    else:
        tmsg.showerror("Error","Invalid Employee ID")

def save_bill():
    op = tmsg.askyesno("Save Reciept","Do you want to save this receipt")
    if(op>0):
        receiptData = receiptArea.get(1.0,END)
        f1 =  open('Receipts/' + f"{Entry_variables.Employee_name.get()}_{Entry_variables.Employee_id.get()}" + '.txt',"w")
        f1.write(receiptData)
        tmsg.showinfo("Saved",f"Your Reciept has been saved with the name : {Entry_variables.Employee_name.get()}_{Entry_variables.Employee_id.get()}")
        f1.close()

def Print():
    receiptData = receiptArea.get(1.0,END)
    fileName = tempfile.mktemp('.txt')
    open(fileName,'w').write(receiptData)
    os.startfile(fileName)

def search():
    con = mysql.connect(host="localhost", user="root",passwd="tiger",database="GLBITM")
    cur = con.cursor()
    lst = []
    query = "Select * from employee;"
    cur.execute(query)
    for i in cur:
        lst.append(i[0])
    if(Entry_variables.Employee_id.get()==""):
        tmsg.showerror("Error","Employee ID not provided!")
    elif(int(Entry_variables.Employee_id.get()) in lst):
        if con.is_connected():
            print("Connection Successfull ....")
            # cur = con.cursor()
            query = f"Select * from employee where Emp_ID = {Entry_variables.Employee_id.get()};"
            cur.execute(query)
            global data
            for data in cur:
                Entry_variables.Employee_name.set(f"{data[1]}")  
                Entry_variables.Basic_pay.set(f"{data[4]}")  
                Entry_variables.Grade_pay.set(f"{data[5]}")  
        else:
            tmsg.showerror("error","Database Not Connected!")
    else:
        tmsg.showerror("Invalid","Invalid Employee Id provided")

def add():
    con = mysql.connect(host="localhost", user="root",passwd="tiger",database="GLBITM")
    if con.is_connected():
        print("Connection Successfull ....")
        lst = []
        cur = con.cursor()
        query = f"Select * from employee;"
        cur.execute(query)
        for i in cur:
            lst.append(i[0])
        if(int(Entry_variables.Employee_id.get()) in lst):
            query = f"update employee set Basic_Pay = {Entry_variables.Basic_Pay.get()} , Grade_Pay = {Entry_variables.Grade_Pay.get()} where Emp_ID = {Entry_variables.Employee_id.get()};"
            cur.execute(query)
            con.commit()
            tmsg.showinfo("Updated","Information has been Updated")
        else:
            a = int(Entry_variables.Employee_id.get())
            print(a)
            query = f"Insert into employee values({a},f'{Entry_variables.Employee_name.get()}','None','None',{Entry_variables.Basic_pay.get()},{Entry_variables.Grade_pay.get()},{Entry_variables.CEA.get()});"
            cur.execute(query)
            con.commit()
            tmsg.showinfo("Successfull","New Record has been added Successfully!")
            
    else:
        tmsg.showerror("error","Database Not Connected!")
        
def remove():
    con = mysql.connect(host="localhost", user="root",passwd="tiger",database="GLBITM")
    cur = con.cursor()
    lst = []
    query = "Select * from employee;"
    cur.execute(query)
    for i in cur:
        lst.append(i[0])
    if(int(Entry_variables.Employee_id.get()) in lst):
        query = f"Delete from employee where Emp_ID = {Entry_variables.Employee_id.get()}"
        cur.execute(query)
        con.commit()
        tmsg.showinfo("Removed","The record has been Successfully Removed")


# Initialising tkinter
root = Tk()
root.geometry("1263x690")
# root.maxsize(1263,690)
root.minsize(1263,690)
root.iconbitmap("Images\\ledgerx-logo.ico")
root.title("LedgerX")


# Background
back = Image.open("Images\\background.png")
resized_back = back.resize((1263,690), Image.ANTIALIAS)
back_image = ImageTk.PhotoImage(resized_back)
# tkinter.Label(root,image=back_image).place(x=0,y=0)
# bg = tkinter.PhotoImage(file="Images//background.png") 
my_canvas = Canvas(root, width=1920, height=1080)
my_canvas.pack(fill="both",expand=True)
my_canvas.create_image(0,0,image=back_image,anchor="nw")


# Logo
picture = Image.open("Images\\ISTE.png")
resized_picture = picture.resize((90,95), Image.ANTIALIAS)
image1 = ImageTk.PhotoImage(resized_picture)
# tkinter.Label(root,image=image,background="#e8e9f0").place(x=750,y=20)
my_canvas.create_image(370,5,image=image1,anchor="nw")


# Menubar
menuBar = Menu(root)
# File Menu
fileMenu = Menu(menuBar,tearoff=0)
fileMenu.add_command(label="New",command=reset)
fileMenu.add_command(label="Save",command=save_bill)
fileMenu.add_separator()
fileMenu.add_command(label="Share",command=Share)
fileMenu.add_separator()
fileMenu.add_command(label="Exit",command=root.destroy)
menuBar.add_cascade(label="File",menu=fileMenu)
# Edit Menu
editMenu = Menu(menuBar,tearoff=0)
editMenu.add_command(label="Undo",command=Undo)
editMenu.add_command(label="Redo",command=Redo)
editMenu.add_separator()
editMenu.add_command(label="Cut",command=lambda : Cut(False))
editMenu.add_command(label="Copy",command=lambda : Copy(False))
editMenu.add_command(label="Paste",command=lambda : Paste(False))
menuBar.add_cascade(label="Edit",menu=editMenu)
# Help Menu
helpMenu = Menu(menuBar,tearoff=0)
helpMenu.add_command(label="About",command=About)
menuBar.add_cascade(label="Help",menu=helpMenu)


# No_of_days (Month):-
No_of_days = StringVar()
No_of_days.set("Select")
dropdown = OptionMenu(root, No_of_days, "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
my_canvas.create_window(380,220,anchor="nw",window=dropdown)

instalment1 = StringVar()
instalment1.set("Instl")
CPF_ins = OptionMenu(root, instalment1, "1", "2", "3", "4", "5", "6","7","8","9","10","11","12","13","14","15","16","17","18","19","20")
my_canvas.create_window(610,540,anchor="nw",window=CPF_ins)
instalment2 = StringVar()
instalment2.set("Instl")
festive_ins = OptionMenu(root, instalment2, "1", "2", "3", "4", "5", "6","7","8","9","10","11","12","13","14","15","16","17","18","19","20")
my_canvas.create_window(610,580,anchor="nw",window=festive_ins)

# Label
my_canvas.create_text(470,20, text="ISTE Payroll System",font="palatino 35 bold" ,anchor="nw")
# tkinter.Label(root ,text="GLBITM Payroll System",background="black",fg="white",font="palatino  35 bold").place(x=880,y=50)
my_canvas.create_text(50,110, text="Employee Id -",font="tahoma 16 italic" ,fill="#4D5382",anchor="nw")
my_canvas.create_text(150,170, text="Name -",font="tahoma 16 bold" ,fill="#4D5382",anchor="nw")
my_canvas.create_text(70,220, text="Month -",font="tahoma 16 " ,anchor="nw")
my_canvas.create_text(70,260, text="Unauthorized Leaves Taken -",font="tahoma 16 " ,anchor="nw")
my_canvas.create_text(70,300, text="Basic Pay -",font="tahoma 16 " ,anchor="nw")
my_canvas.create_text(70,340, text="Grade Pay -",font="tahoma 16 " ,anchor="nw")
my_canvas.create_text(70,380, text="CEA -",font="tahoma 16 " ,anchor="nw")
my_canvas.create_text(70,420, text="Others -",font="tahoma 16 " ,anchor="nw")
my_canvas.create_text(70,460, text="Total Deduction -",font="tahoma 16 " ,anchor="nw")
my_canvas.create_text(70,500, text="Income Tax -",font="tahoma 16 " ,anchor="nw")
my_canvas.create_text(70,540, text="CPF Advance -",font="tahoma 16 " ,anchor="nw")
my_canvas.create_text(70,580, text="Festival Advance -",font="tahoma 16 " ,anchor="nw")

# Entries
class Entry_variables():
    Employee_id = StringVar()
    Employee_name = StringVar()
    Basic_pay = IntVar()
    Grade_pay = IntVar()
    CEA = IntVar()
    Others = IntVar()
    total_deduction = IntVar()
    income_tax = IntVar()
    CPF_amount = IntVar()
    festive_amount = IntVar()

Employee_id_entry = Entry(root,textvariable=Entry_variables.Employee_id,font="tahoma 15",width=35,relief="sunken",bg="#4D5382",fg="white")
Employee_name_entry = Entry(root,textvariable=Entry_variables.Employee_name,font="tahoma 15",relief="sunken",width=35)
Basic_pay_entry = Entry(root,textvariable=Entry_variables.Basic_pay,font="tahoma 15",relief="sunken")
Grade_pay_entry = Entry(root,textvariable=Entry_variables.Grade_pay,font="tahoma 15",relief="sunken")
CEA_entry = Entry(root,textvariable=Entry_variables.CEA,font="tahoma 15",relief="sunken")
Others_entry = Entry(root,textvariable=Entry_variables.Others,font="tahoma 15",relief="sunken")
total_deduction_entry = Entry(root,textvariable=Entry_variables.total_deduction,font="tahoma 15",relief="sunken")
income_tax_entry = Entry(root,textvariable=Entry_variables.income_tax,font="tahoma 15",relief="sunken")
CPF_amount_entry = Entry(root,textvariable=Entry_variables.CPF_amount,font="tahoma 15",relief="sunken")
festive_amount_entry =Entry(root,textvariable=Entry_variables.festive_amount,font="tahoma 15",relief="sunken")

my_canvas.create_window(200,110,anchor="nw",window=Employee_id_entry)
my_canvas.create_window(240,167,anchor="nw",window=Employee_name_entry)
my_canvas.create_window(380,300,anchor="nw",window=Basic_pay_entry)
my_canvas.create_window(380,340,anchor="nw",window=Grade_pay_entry)
my_canvas.create_window(380,380,anchor="nw",window=CEA_entry)
my_canvas.create_window(380,420,anchor="nw",window=Others_entry)
my_canvas.create_window(380,460,anchor="nw",window=total_deduction_entry)
my_canvas.create_window(380,500,anchor="nw",window=income_tax_entry)
my_canvas.create_window(380,540,anchor="nw",window=CPF_amount_entry)
my_canvas.create_window(380,580,anchor="nw",window=festive_amount_entry)

# Spinbox
leave = StringVar()
Unauthorized_leave = Spinbox(root,from_=0,to=31,font="tahoma 15",textvariable=leave)
my_canvas.create_window(380,260,anchor="nw",window=Unauthorized_leave)


# Buttons
find = Button(root,font="tahoma 10",text="Search",command=search)
my_canvas.create_window(589,108,anchor="nw",window=find)

save_button = Button(root,font="vertica 14",width=14,text="Save",command=save_bill,background="#8CBA80",fg="white")
my_canvas.create_window(80,620,anchor="nw",window=save_button)
Reset_button = Button(root,font="vertica 14",width=14,text="Reset",command=reset,background="#FB4D3D",fg="white")
my_canvas.create_window(280,620,anchor="nw",window=Reset_button)
Generate_button = Button(root,font="vertica 14",width=14,text="Generate Receipt",command=generate_receipt,background="#2D2D2A",fg="white")
my_canvas.create_window(480,620,anchor="nw",window=Generate_button)

Add_button = Button(root,font="vertica 15",width=12,text="Add",command=add,background="#2D2D2A",fg="white")
my_canvas.create_window(700,100,anchor="nw",window=Add_button)
Remove_button = Button(root,font="vertica 15",width=12,text="Remove",command=remove,background="#2D2D2A",fg="white")
my_canvas.create_window(860,100,anchor="nw",window=Remove_button)

print_button = Button(root,font="vertica 13",width=10,text="Print",command=Print,background="#2D2D2A",fg="white")
my_canvas.create_window(1125,632,anchor="nw",window=print_button)
send_button = Button(root,font="vertica 13",width=10,text="send",command=button_definitions.send,background="#2D2D2A",fg="white")
my_canvas.create_window(1015,632,anchor="nw",window=send_button)


# Lines
my_canvas.create_line(50,145,680,145)  # top
my_canvas.create_line(50,145,50,630)   # left
my_canvas.create_line(50,630,680,630)  # bottom
my_canvas.create_line(680,145,680,630) # right

# Reciept Generation
receiptArea = Text(root,bg="white",fg="blue",width=65,height=30)
my_canvas.create_window(700,145,anchor="nw",window=receiptArea)

root.config(menu=menuBar)

# Function Call
welcome()


root.mainloop()