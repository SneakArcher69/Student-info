import os
import re
import sys
import time
import shelve
import winsound
import warnings
import mysql.connector as sql
from tabulate import tabulate
from termcolor import colored
from datetime import datetime
from getpass import getpass as pas

# To ignore any unexpected warnings
warnings.filterwarnings("ignore")

# Error sound
def beep():
    winsound.PlaySound("null", winsound.SND_ASYNC)

# Stylish printing
def flow(string):
    for x in string:
        if x == '-' or x == '+' or x == '|':
            print(x, end='')
            continue
        if x == string[-1]:
            sys.stdout.write(x)
            sys.stdout.flush()
        else:
            sys.stdout.write(x)
            sys.stdout.flush()
            time.sleep(0.005)

# More stylish printing
def flowz(string):
    for x in string:
        if x == string[-1]:
            sys.stdout.write(x)
            sys.stdout.flush()
        else:
            sys.stdout.write(x)
            sys.stdout.flush()
            time.sleep(0.05)

# Font colors
def green(string):
    return colored(string, "green", attrs=['bold'])

def yellow(string):
    return colored(string, "yellow", attrs=['bold'])

def cyan(string):
    return colored(string, "cyan", attrs=['bold'])

def red(string):
    return colored(string, "red", attrs=['bold'])

def blue(string):
    return colored(string, "blue", attrs=['bold'])


# Main intro
def banner():
    banr = '''
             ╦  ╦ ╔═╗  ═╦═        STUDENT
             ║  ║ ╚═╗   ║         INFORMATION
             ╩  ╩ ╚═╝ ╚═╝         SYSTEM
          '''
    print(cyan(banr))

# For borders
def border_msg(msg):
    row = len(msg)
    m = ''.join(['        +'] + ['-' * row] + ['+'])
    h = cyan(m)
    result = h + '\n' + \
        cyan("        |") + (msg) + \
        cyan("|") + '\n' + h
    flow((result))
    print()


# Symbols
smb = {
    "WARN": " ⚠️  ",
    "DONE": " ✅ ",
    "INPUT": cyan(" [»] "),
    "INFO": yellow(" [!] "),
    "ARROW": cyan(" > ")
}

# Choice menu
def display_menu():
    flow("\n" + smb["ARROW"] + cyan("CHOOSE AN OPTION :") + "\n\n")
    print(smb["ARROW"] + yellow("[1] ") + ("Add New Student"))
    print(smb["ARROW"] + yellow("[2] ") + ("Remove Student"))
    print(smb["ARROW"] + yellow("[3] ") + ("Erase all records"))
    print(smb["ARROW"] + yellow("[4] ") + ("Search Record"))
    print(smb["ARROW"] + yellow("[5] ") + ("View all Records"))
    print(smb["ARROW"] + yellow("[6] ") + ("Sort Records"))
    print(smb["ARROW"] + yellow("[7] ") + ("Quit Program"))
    print(smb["ARROW"] + yellow("[8] ") + ("About Developers"))


# For clearing screen
def clr_scr():
    _ = os.system('cls')

def qui():
    print()
    flow(smb["WARN"] + red("Quitting....\n"))
    time.sleep(0.2)
    winsound.PlaySound(r"./sfx/quit.wav", winsound.SND_ASYNC)
    flow(smb["WARN"] + red("Program quit.\n"))
    time.sleep(1)
    clr_scr()
    sys.exit()

# Connecting to MySQL instance
def connect():
    qwerty=os.path.exists(r'.\config')
    if qwerty:
        pass
    else:
        os.makedirs(r'.\config')
    config=shelve.open(r'config\config')
    while True:
        try:
            try:
                user_=config['user']
            except KeyError:
                user_ = input(smb["INPUT"]+blue('Enter MySql User [\'root\' by default]: '))
                condition = True
            else:
                condition = False
            pin = pas(prompt=smb["INPUT"]+blue('Enter MySql Password : '))
        except KeyboardInterrupt:
            qui()
        try:
            cnx = sql.connect(host='localhost', user=user_, password=pin)
        except sql.errors.ProgrammingError:
            beep()
            if condition:
                print(smb["INFO"]+yellow("Please make sure you entered username and password correctly"))
            else:
                print(smb["INFO"]+yellow("Please make sure you entered password correctly"))
            continue
        if cnx.is_connected():
            config['user']=user_
            winsound.PlaySound(r"./sfx/login.wav", winsound.SND_ASYNC)
            wer = smb["DONE"]+green("Authorised")
            flow(wer)
            time.sleep(1.5)
            print()
            global cursor
            cursor = cnx.cursor()
            # Creating database
            while True:
                try:
                    try:
                        global con
                        dbin=config['db']
                    except KeyError:
                        con = True
                        dbin = input(smb["INPUT"]+blue('Enter the Database name [an unused or not created db name]  : '))
                    else:
                        con = False
                    cursor.execute(f'CREATE DATABASE IF NOT EXISTS {dbin};')
                    global cnxz
                    cnxz = sql.connect(host='localhost', user=user_,
                            password=pin, database=dbin)
                except KeyboardInterrupt:
                    qui()
                except sql.errors.ProgrammingError:
                    beep()
                    print(
                        smb["INFO"]+yellow("Please make sure you entered a valid Database name"))
                    continue
                break
            config['db']=dbin
            config.close()           
            cursor = cnxz.cursor()
            print()
            print("\n")
            clr_scr()
            break
        else:
            beep()
            print(
                smb["INFO"]+yellow("Please make sure you entered the password correctly"))
            continue

# Creating tables
def table():
    if con:
        a = '''Create Table if not exists Student_Record(
            GrNo bigint Primary key,
            Name varchar(41) NOT NULL,
            DOB date NOT NULL,
            Class char(5) NOT NULL,
            Division varchar(5) NOT NULL,
            Phone varchar(15) NOT NULL unique,
            Email varchar(51) NOT NULL unique,
            Stream varchar(15) 
            );'''
        b = '''Create Table if not exists Transport(
            GrNo bigint Primary key,
            Name varchar(41) NOT NULL,
            Phone varchar(15) NOT NULL unique,
            Bus int NOT NULL,
            City varchar(15) NOT NULL,
            District varchar(51) NOT NULL,
            Street varchar(51) NOT NULL,
            Building int NOT NULL,
            FOREIGN KEY (GrNo) REFERENCES Student_Record(GrNo)
            );'''
        cursor.execute(a)
        cursor.execute(b)
    else:
        pass


# For entering and validating name
def name_():
    name = input(smb["INPUT"]+blue("Enter the name of the Student : "))
    if name.replace(' ', '').isalpha() == True and len(name) < 40:
        return name.title()
    else:
        beep()
        print(smb["INFO"]+yellow("Name cannot contain numbers or other symbols and must be seperated by a single space."+'\n' +
                                 smb["INFO"]+yellow("Max length is 40 characters")))
        return None

# For entering and validating grNo.
def GrNo_():
    try:
        GrNo = int(
            input(smb["INPUT"]+blue("Enter GrNo. of the Student : ")))
    except TypeError and ValueError:
        beep()
        print(smb["INFO"]+yellow("Please Enter a valid GrNo."))
        return None
    if GrNo > 0 and GrNo < 150000:
        pass
    else:
        beep()
        print(smb["INFO"]+yellow("GrNo should be between 0 and 150000"))
        return None
    cursor.execute("select GrNo from student_Record")
    reg = cursor.fetchall()
    tup = (GrNo,)
    if tup not in reg:
        return GrNo
    else:
        beep()
        print(smb["INFO"]+yellow("GrNo already exists"))
        return None

def DOB():
    date=input(smb["INPUT"]+blue("Enter date of birth [dd-mm-yyyy]: "))
    a=re.compile(r"""^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|
    30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|
    \.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|
    [3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|
    [2-9]\d)?\d{2})$""",re.X)
    current = datetime.now().year
    upperbound= current - 3
    lowerbound= current - 21
    if a.search(date) and len(date) == 10:
        year = int(date[-4:])
    else :
        print(smb["INFO"] + yellow("Please enter a valid date"))
        return None
    if year > lowerbound and year < upperbound:
        string= date[-4:] + "-" + date[3:5] + "-" + date[:2]
        return string
    else:
        print(smb["INFO"] + yellow(f"Year can't be lower than {lowerbound+1} and can't be higher than {upperbound-1}"))
        return None
# For entering and validating class
def clas_():
    sd = ["1","2","3","4","5","6","7","8","9","10","11","12","LKG","UKG"]
    global clas
    clas = input(smb["INPUT"]+blue("Enter the class of the student : "))
    if clas.upper() not in sd:
        beep()
        print(smb["INFO"]+yellow("Enter valid class[LKG, UKG, 1-12]"))
        return None
    else:
        if len(clas) == 1:
            clas = "0"+clas
            return clas
        else:
            return clas.upper()

# For entering and validating division
def div_():
    divs = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12',
            'B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B09', 'B10', 'B11', 'B12']
    div = input(smb["INPUT"]+blue("Enter class division : "))
    if div.upper() in divs:
        return div.upper()
    else:
        beep()
        print(
            smb["INFO"]+yellow("Please Enter Valid Division[A01-A12,B01-B12]"))
        return None

# For validating phone number
def check_(_phone):
    _regex = r'[05]\d\d\d\d\d\d\d\d\d\Z'
    if re.match(_regex, _phone):
        return True
    else:
        return False

# For entering phone number
def phone_():
    try:
        phone = input(
            smb["INPUT"]+blue("Enter Phone Number [Starting with 05] : "))
    except TypeError and ValueError:
        beep()
        print(
            smb["INFO"]+yellow("Please Enter a valid Mobile Number. Ex:0512345678"))
        return None
    cursor.execute("select phone from student_Record")
    reg_ = cursor.fetchall()
    tup_ = ('+966'+phone[1:],)
    if tup_ not in reg_:
        confirm = True
    else:
        confirm = False
        beep()
        print(
            smb["INFO"]+yellow("Mobile Number already registered with another student."))
        return None
    if check_(phone) == True and confirm == True:
        phone = phone[1:]
        phone = '+966'+phone
        return phone
    else:
        beep()
        print(
            smb["INFO"]+yellow("Please Enter a valid Mobile Number. Ex:0512345678"))
        return None

# For validating email
def check(_email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.match(regex, _email):
        return True
    else:
        return False

# For entering email
def email_():
    email = input(
        smb["INPUT"]+blue("Enter Email address of the Student : "))
    cursor.execute("select email from student_Record")
    _reg_ = cursor.fetchall()
    _tup_ = (email,)
    if _tup_ not in _reg_:
        confirm = True
    else:
        confirm = False
        beep()
        print(smb["INFO"]+yellow("Email adress already registered in database"))
        return None
    if check(email) == False:
        beep()
        print(smb["INFO"]+yellow("Please Enter valid email address"))
        return None
    if check(email) == True and confirm == True:
        return email
    else:
        return None

# For entering and validating stream
# Stream is only asked if the class given is 11 or 12.
def stream_():
    if clas in ["11","12"]:
        stream = input(smb["INPUT"]+blue("Enter the Stream : "))
        if stream.lower() in ['science', 'commerce']:
            return stream.upper()
        else:
            beep()
            print(smb["INFO"]+yellow("Please enter 'Science' or 'Commerce'"))
            return None
    else:
        return None

# Asking if transport details are to be entered
def Transport():
    prompt = input(
        smb["INPUT"]+blue("Do you wish to enter Transportation details ? ['Y' or 'Yes']: "))
    if prompt.lower() in ['yes', 'y']:
        return True
    else:
        pass

# For entering and validating bus no
def bus():
    try:
        prompt = int(
            input(smb["INPUT"]+blue("Enter Bus Number [0-300] : ")))
    except TypeError and ValueError:
        beep()
        print(smb["INFO"]+yellow("Please Enter a valid Bus No"))
        return None
    if prompt < 0 or prompt > 300:
        beep()
        print(smb["INFO"]+yellow("Please Enter a valid Bus No between 0 and 300"))
        return None
    else:
        return prompt

# For entering and validating city
def city():
    prompt = input(smb["INPUT"]+blue("Enter the city of residence : "))
    if prompt.lower() not in ['jeddah', 'makkah']:
        beep()
        print(
            smb["INFO"]+yellow("Transport service available in Jeddah and Makkah only"))
        return None
    else:
        return prompt.title()

# For entering and validating district
def district():
    prompt = input(
        smb["INPUT"]+blue("Enter the district of residence : "))
    if prompt.replace(' ', '').isalpha() == False and len(prompt) < 50:
        beep()
        print(smb["INFO"]+yellow("Please enter a valid District Name"))
        return None
    else:
        return prompt.title()

# For entering and validating building no
def Building_no():
    try:
        prompt = int(
            input(smb["INPUT"]+blue("Enter Building No [Max 5 Digit] : ")))
    except TypeError and ValueError:
        beep()
        print(smb["INFO"]+yellow("Please Enter a valid Building No"))
        return None
    if prompt < 0 or prompt > 99999:
        beep()
        print(smb["INFO"]+yellow("Please Enter a valid Building No"))
        return None
    else:
        return prompt

# For entering and validating street 
def street():
    prompt = input(
        smb["INPUT"]+blue("Enter the street name of residence : "))
    if prompt.replace(' ', '').isalpha() == False and len(prompt) < 50:
        beep()
        print(smb["INFO"]+yellow("Please enter a valid street name"))
        return None
    else:
        return prompt.title()

# Add a Student
def add():
    while True:
        GrNo = GrNo_()
        if GrNo == None:
            continue
        else:
            break
    while True:
        name = name_()
        if name == None:
            continue
        else:
            break
    while True:
        dob = DOB()
        if dob == None:
            continue
        else:
            break
    while True:
        clas = clas_()
        if clas == None:
            continue
        else:
            break
    while True:
        div = div_()
        if div == None:
            continue
        else:
            break
    while True:
        phone = phone_()
        if phone == None:
            continue
        else:
            break
    while True:
        email = email_()
        if email == None:
            continue
        else:
            break
    while True:
        stream = stream_()
        if clas in ["11","12"] and stream == None:
            continue
        else:
            break
    lst = [GrNo, name, dob, clas, div, phone, email, stream]
    if None not in lst:
        a = f"Insert into Student_Record values({GrNo},'{name}','{dob}','{clas}','{div}','{phone}','{email}','{stream}');"
    elif lst[-1] is None and lst[:5] is not None:
        a = f"Insert into Student_Record values({GrNo},'{name}','{dob}','{clas}','{div}','{phone}','{email}',NULL);"
    else:
        beep()
        print(
            smb["WARN"]+red("Something went wrong. Please make sure you entered everything correctly."))
        return None
    cursor.execute(a)
    cnxz.commit()
    print(smb["DONE"]+green("Succesfully entered data."))
    transport = Transport()
    if transport is True:
        while True:
            Bus_No = bus()
            if Bus_No == None:
                continue
            else:
                break
        while True:
            cityz = city()
            if cityz == None:
                continue
            else:
                break
        while True:
            districtz = district()
            if districtz == None:
                continue
            else:
                break
        while True:
            streetz = street()
            if streetz == None:
                continue
            else:
                break
        while True:
            Building_noz = Building_no()
            if Building_noz == None:
                continue
            else:
                break
        a = f"Insert Transport values({GrNo},'{name}','{phone}',{Bus_No},'{cityz}','{districtz}','{streetz}',{Building_noz});"
        cursor.execute(a)
        cnxz.commit()
        print(smb["DONE"]+green("Succesfully entered transportation data."))
    return True


# Checking if a grno is already in Database
def __GrNo_():
    try:
        GrNo = int(
            input(smb["INPUT"]+blue("Enter GrNo. of the Student :")))
    except TypeError and ValueError:
        beep()
        print(smb["INFO"]+yellow("Please Enter a valid GrNo."))
        return None
    cursor.execute("select GrNo from student_Record")
    reg = cursor.fetchall()
    tup = (GrNo,)
    if tup not in reg:
        beep()
        print(smb["INFO"]+yellow(str(GrNo) +
              ' is not registered in the Database '))
        return None
    else:
        return GrNo

# Checking if a student has transportation details
def gragain(x):
    GrNo = x
    cursor.execute("select GrNo from Transport")
    reg = cursor.fetchall()
    tup = (GrNo,)
    if tup not in reg:
        beep()
        print(smb["INFO"]+yellow(str(GrNo) +
              ' does not avail School Transportation '))
        return None
    else:
        return GrNo

# Remove Student
def remove():
    GrNo = __GrNo_()
    if GrNo != None:
        b = f"DELETE FROM transport WHERE GrNo={GrNo}"
        a = f"DELETE FROM Student_record WHERE GrNo={GrNo}"
    else:
        return None
    cursor.execute(b)
    cnxz.commit()
    cursor.execute(a)
    cnxz.commit()
    print(smb["DONE"]+green(f"Succesfully removed GrNo {GrNo}"))

# Delete all records.
def del_all():
    prompt = input(smb["INPUT"] + smb["WARN"] + smb["WARN"] + smb["WARN"] + red(
                   "Are you sure you want to delete all records?\n" + smb["INPUT"] + smb["WARN"] + smb["WARN"] + 
                   smb["WARN"]+red("They cannot be recovered! Type 'CONFIRM' to confirm : ")))
    if prompt == 'CONFIRM':
        a = 'Delete from student_record'
        b = 'Delete from transport'
        cursor.execute(b)
        cnxz.commit()
        cursor.execute(a)
        cnxz.commit()
        print(smb["DONE"]+green("Removed all existing records."))
    else:
        beep()
        print(smb["WARN"]+"Action Aborted")

# View a student's details
def view():
    temp = list()
    GrNo = __GrNo_()
    if GrNo != None:
        a = f"select * from student_record where GrNo={GrNo}"
    else:
        return None
    cursor.execute(a)
    x = cursor.fetchall()
    lst = list(x[0])
    print('  Name    : ', lst[1])
    print('  GrNo    : ', lst[0])
    print('  Class   : ', lst[2])
    print('  Section : ', lst[3])
    print('  Phone   : ', lst[4])
    print('  Email   : ', lst[5])
    if lst[-1] is not None:
        print('  Stream  : ', lst[6])
    else:
        pass
    if gragain(GrNo) != None:
        b = f"select * from transport where GrNo={GrNo}"
    else:
        return None
    cursor.execute(b)
    y = cursor.fetchall()
    ltt = list(y[0])
    print('  Bus No. : ', ltt[3])
    print('  Address : ', str(ltt[7])+' ' + ltt[6]+', ' + ltt[5]+', ' + ltt[4])

# View a student's transportation details
def view_transport():
    temp = list()
    cursor.execute("Select * from transport")
    x = cursor.fetchall()
    for y in x:
        temp.append(list(y))
    print(tabulate(temp, headers=[
        'GrNo', 'Name', 'Phone', 'Bus', 'City', 'District', 'Street', 'Building'], tablefmt='outline'))

# Display entire table
def view_all():
    temp = list()
    cursor.execute("Select * from Student_Record")
    x = cursor.fetchall()
    for y in x:
        temp.append(list(y))
    for lists in temp:
        count = -1
        for elemt in lists:
            count += 1
            if elemt == None:
                lists[count] = 'NULL'
            else:
                continue
        del count
    print(tabulate(temp, headers=[
          'GrNo', 'Name','Date of Birth', 'Class', 'Division', 'Phone', 'Email', 'Stream'], tablefmt='outline'))
    prompt = input(
        smb["INPUT"]+blue("Do you want to display Transportation Details ? ['Y' or 'Yes']: "))
    if prompt.lower() in ['yes', 'y']:
        view_transport()
    else:
        beep()
        pass

# Sort table transport
def sortz():
    lst = ['grno', 'name', 'class', 'city', 'phone',
           'district', 'street', 'Bus_No', 'Building_No']
    user = input(
        smb["INPUT"]+blue("Enter the order of sorting objects [Ex: street city] : "))
    a = user.split()
    if user.isspace() is True or user == None:
        return None
    for i in a:
        if i.lower() not in lst or len(a) > 7:
            beep()
            print(
                smb["INFO"]+yellow("Please enter valid column names seperated by a single space."))
            return None
        else:
            continue
    string = ''
    for u in a:
        string += u+','
    string = string[:-1]
    temp = list()
    if string.isspace() == False and string != '':
        cursor.execute(f"Select * from Transport order by {string}")
        x = cursor.fetchall()
        for y in x:
            temp.append(list(y))
        print(tabulate(temp, headers=[
            'GrNo', 'Name','Phone', 'Bus_No', 'City', 'District', 'Street Name', 'Building_No'], tablefmt='outline'))

# Sort table
def sort():
    prompt = input(
        smb["INPUT"]+blue("Which table is to be sorted? ? [Student(default) or Transport]: "))
    if prompt.lower() == 'student':
        pass
    elif prompt.lower() == 'transport':
        sortz()
        return True
    else:
        print(smb["INFO"]+green('Invalid Input. Sorting Student Table'))
        beep()
    lst = ['grno', 'name', 'class', 'division', 'phone', 'email', 'stream']
    user = input(
        smb["INPUT"]+blue("Enter the order of sorting objects [Ex:grno class] : "))
    a = user.split()
    if user.isspace() is True or user == None:
        beep()
        return None
    for i in a:
        if i.lower() not in lst or len(a) > 7:
            beep()
            print(
                smb["INFO"]+yellow("Please enter valid column names seperated by a single space."))
            return None
        else:
            continue
    string = ''
    for u in a:
        string += u+','
    string = string[:-1]
    temp = list()
    if string.isspace() == False and string != '':
        cursor.execute(f"Select * from Student_Record order by {string}")
        x = cursor.fetchall()
        for y in x:
            temp.append(list(y))
        for lists in temp:
            count = -1
            for elemt in lists:
                count += 1
                if elemt == None:
                    lists[count] = 'NULL'
                else:
                    continue
            del count
        print(tabulate(temp, headers=[
            'GrNo', 'Name','Date of Birth', 'Class', 'Division', 'Phone', 'Email', 'Stream'], tablefmt='outline'))

# Quit Program
def quitz():
    cnxz.close()
    print()
    flow(smb["WARN"] + red("Quitting....\n"))
    time.sleep(0.2)
    winsound.PlaySound(r"./sfx/quit.wav", winsound.SND_ASYNC)
    flow(smb["WARN"] + red("Program quit.\n"))
    time.sleep(1)
    clr_scr()
    sys.exit()

# For printing developer credits stylishly
def pprint(string):
    for i in range(1, 3):
        time.sleep(0.2)
        print('')
    flowz(string.center(120))

# Developer credits
def about():
    winsound.PlaySound(r"./sfx/outro.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
    print("***********************************************************************".center(120))
    pprint("INTERNATIONAL INDIAN SCHOOL JEDDAH")
    pprint("Mr Qurban Khan")
    pprint("XII B05")
    pprint("Muhammed Nabeel")
    pprint("Abdullah Shihavudeen")
    pprint("Sayed Afnan")
    pprint("All Rights to Nabs™ 2023 ©")
    print()
    print()
    print()
    print("***********************************************************************".center(120))
    winsound.PlaySound(None, winsound.SND_ASYNC)
    time.sleep(3)
    clr_scr()

# Getting choice input
def mainz():
    while True:
        banner()
        display_menu()
        func = int(input(smb["INPUT"]))
        print()
        if func == 1:
            try:
                add()
            except TypeError and ValueError:
                beep()
                print(smb["INFO"]+yellow("Please Enter valid data."))
            except sql.errors.IntegrityError:
                beep()
                print(
                    smb["INFO"]+yellow("Duplicate data was entered for unique columns."))

        elif func == 2:
            remove()
        elif func == 3:
            del_all()
        elif func == 4:
            view()
        elif func == 5:
            view_all()
        elif func == 6:
            sort()
        elif func == 8:
            about()
        elif func == 7:
            quitz()
        else:
            beep()
            print(smb["INFO"]+cyan("Please Enter 1, 2, 3, 4, 5, 6, 7 or 8."))
        print()
        input(smb["ARROW"]+green("Press Enter to continue . . . \n"))
        clr_scr()

# Loopin main program
def main():
    while True:
        try:
            mainz()
        except EOFError and KeyboardInterrupt:
            beep()
            clr_scr()
            print()
            continue
        except ValueError:
            beep()
            print(smb["INFO"]+yellow("Please enter a valid input."))
            input(smb["ARROW"]+green("Press Enter to continue . . . \n"))
            clr_scr()
            continue
        except AttributeError as df:
            beep()
            print(smb["INFO"]+red("There was an Attribute Error"))
            print(red(df))
            input(smb["ARROW"]+green("Press Enter to continue . . . \n"))
            clr_scr()
            continue

# Start Program
def start():
    clr_scr()
    connect()
    table()
    border_msg(" Welcome To Student Information System")

# Finally calling the functions
start()
main()
