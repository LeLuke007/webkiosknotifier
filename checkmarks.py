import requests
import smtplib
import os

with requests.Session() as c:
    loginurl='https://webkiosk.thapar.edu/CommonFiles/UserAction.jsp'
    marksurl="https://webkiosk.thapar.edu/StudentFiles/Exam/StudentEventMarksView.jsp?x=&exam=2324ODDSEM"
    headers={
    "Connection": "keep-alive",
    "Origin": "https://webkiosk.thapar.edu",
    "Referer": "https://webkiosk.thapar.edu/",
    }
    logindata={
    "txtuType": "Member Type",
    "UserType": "S",
    "txtCode": "Enrollment No",
    "MemberCode": os.getenv("RollNumber"),
    "txtPin": "Password/Pin",
    "Password": os.getenv("WebkioskPassword"),
    }
    c.post(loginurl,logindata,headers)
    page=c.get(marksurl)
    tr= int(page.text.count('<tr>')-4)

    with open("currentVal.txt","w") as f:
        f.write(str(tr))
    
    while(True):
        with open("currentVal.txt","r") as f:
            current=int(f.read())
        c.post(loginurl,logindata,headers)
        page=c.get(marksurl)
        tr= int(page.text.count('<tr>')-4)
        if tr>current:
            try:
                msg = """Subject: New Marks Uploaded """
                fromaddr = os.getenv("emailID")
                password = os.getenv("emailIDPassword")
                with open("maillist.txt","r") as f:
                    toaddrs=f.read().strip().split("\n")
        
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.login(fromaddr, password)
        
                server.sendmail(fromaddr, toaddrs, msg)
                with open("currentVal.txt","w") as f:
                    f.write(str(tr))
                server.quit()
                print("Marks Uploaded",tr)
            except:
                print("Error Occured While Sending Mail")
                server.quit()
