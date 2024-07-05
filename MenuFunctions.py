# Modules
from tkinter import messagebox as tmsg

# Menu Functions

# File Menu
# New Function has been defined by the name of Reset in the button section
def reset():
    print("Hello World!!")
def Save():
    pass
def Share():
    email_Sender = ''
    email_Password = ''
    email_Receiver = ''

    subject = f"Paycheck Receipt for {No_of_days.get()}"
    body = " Payreceipt Generated"

    em = EmailMessage()
    em['From'] = email_Sender
    em['To'] = email_Receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com',465, context) as smtp:
        smtp.login(email_Sender,email_Password)
        smtp.sendmail(email_Sender,email_Receiver,em.as_string())

# Edit Menu
def Undo():
    pass
def Redo():
    pass
def Cut(e):
    global selected
    if my_text.selection_get():
        selected = my_text.selection_get()
        my_text.delete("sel.first","sel.last")

def Copy(e):
    global selected
    if my_text.selection_get():
        selected = my_text.selection_get()

def Paste(e):
    if selected:
        position = my_text.index(INSERT)
        my_text.insert(position,selected)

# Help Menu
def About():
    tmsg.showinfo("GLBITM Payroll System","Version : 1.0\nCommit : 0668fed0c5baa5f6d004a71de3937055985e2638\nDeveloped by : Mukul Jain")