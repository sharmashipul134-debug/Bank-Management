import json
import random
import string
from pathlib import Path


class Bank:
    database='data.json'
    data=[]

    try:
        if Path(database).exists():
            with open(database) as fs:
                data=json.loads(fs.read())
        else:
            print("no such file exsist ")
    except Exception as err:
        print(f"an exception occured as {err}")

    @classmethod
    def __update(cls):
        with open(cls.database,'w') as fs:
            fs.write(json.dumps(Bank.data))
    @classmethod
    def __accountgenerate(cls):
        alpha=random.choices(string.ascii_letters,k=3)
        num=random.choices(string.digits,k=3)
        spchar=random.choices("!@#$%^&*",k=1)
        id=alpha+num+spchar
        random.shuffle(id)
        return"".join(id)


    def createaccount(self):
        info={
            "name":input("enter your name:-"),
            "age":int(input("enter your age:-")),
            "email":(input("enter your email:-")),
            "pin":int(input("enter your 4 digits pin:-")),
            "AccountNo.":Bank.__accountgenerate(),
            "balance":0
        }
        if info['age']<18 or len(str(info['pin']))!=4:
            print("sorry cannot create your account")
        else:
            print("account has been created successfully")
            for i in info:
                print(f"{i} :{info[i]}")
            print("please note down your account number")

            Bank.data.append(info)
            Bank.__update()

    def depositmoney(self):
        accnumber=input("please enter your account number ")
        pin=int(input("please enter your 4 digits pin "))

        userdata=[i for i in Bank.data if i['AccountNo.']==accnumber and i['pin']==pin]

        if userdata==False:
            print("sorry no data is found")
        else:
            amount=int(input("how much you want to deposit  "))
            if amount>10000 or amount<0:
                print("sorry the amount is too much you can deposit below 10000 and above 0")

            else:
                userdata[0]['balance']+=amount
                Bank.__update()
                print("Amount deposited successfully")



    def withdrawmoney(self):
            accnumber=input("please enter your account number ")
            pin=int(input("please enter your 4 digits pin "))
    
            userdata=[i for i in Bank.data if i['AccountNo.']==accnumber and i['pin']==pin]
    
            if userdata==False:
                print("sorry no data is found")
            else:
                amount=int(input("how much you want to withdraw "))
                if userdata[0]['balance']<amount:
                    print("sorry you do not have that much balance in your bank account")
    
                else:
                    userdata[0]['balance']-=amount
                    Bank.__update()
                    print("Amount withdraw successfully")

    def showdetails(self):
        accnumber=input("please enter your account number ")
        pin=int(input("please enter your 4 digits pin "))
        userdata=[i for i in Bank.data if i['AccountNo.']==accnumber and i['pin']==pin]
        print("your information are \n\n\n")
        for i in userdata[0]:
            print(f"{i}:{userdata[0][i]}")

    def updatedetails(self):
         accnumber=input("please enter your account number ")
         pin=int(input("please enter your 4 digits pin "))

         userdata=[i for i in Bank.data if i['AccountNo.']==accnumber and i['pin']==pin]
         if userdata==False:
            print("sorry no such user is found")

         else:
             print("you cannot change the age,balance,and account number")
             print("Fill the details for change or leave ot empty if no change")

             newdata= {
                 "name":input("please tell your new nameor press enter:"),
                 "email":input("please tell your new email or press enter to skip:"),
                 "pin":input("enter new pin or press enter to skip:")
                 
                }

             if newdata["name"]=="":
                 newdata["name"]=userdata[0]['name']
             if newdata["email"]=="":
                newdata["email"]=userdata[0]['email']
             if newdata["pin"]=="":
                 newdata["pin"]=userdata[0]['pin']

             newdata['age']=userdata[0]['age']
             newdata['AccountNo.']=userdata[0]['AccountNo.']
             newdata['balance']=userdata[0]['balance']

             if type(newdata['pin'])==str:
                 newdata['pin']=int(newdata['pin'])

             for i in newdata:
                 if newdata[i]==userdata[0][i]:
                     continue
                 else:
                     userdata[0][i]=newdata[i]

             Bank.__update()
             print("details updates successfully")
         
                 
        



    pass

user=Bank()
print("press 1 for creating an account")
print("press 2 for depositing the money in the bank")
print("press 3 for withdrawing the money")
print("press 4 for details")
print("press 5 for updating the details")
print("press 6 for deleting the account ")

check=int(input("tell your response:-"))

if check==1:
    user.createaccount()

if check==2:
    user.depositmoney()

if check==3:
    user.withdrawmoney()

if check==4:
    user.showdetails()

if check==5:
    user.updatedetails()