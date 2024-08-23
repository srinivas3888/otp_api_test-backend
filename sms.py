from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import smtplib
from email.message import EmailMessage
import random
import json
import os

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. You can replace "*" with a specific domain if needed.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods. You can restrict to specific methods if needed.
    allow_headers=["*"],  # Allows all headers. You can restrict to specific headers if needed.
)


global otp_g
otp_g=""
global data
data=dict()

def generate_otp() -> str:
    global otp_g
    otp_g = str( random.randrange(1000, 9999) )
    return otp_g

def verify_user(email) -> bool:
    f='data.json'
    if os.path.exists(f):
        fp=open(f, 'r')
        global data
        data=json.load(fp)
        fp.close()
    else:
        fp=open(f, 'w')
        x=dict()
        json.dump(x, fp, indent=4)
        fp.close()
        
    try:
        global data
        d=data[str(email)]
        return True
    except:
        return False
    
def store_user(name, email) -> None:
    f=open("data.json", "w")
    global data
    data[str(email)]=str(name)
    json.dump(data, f, indent=4)
    f.close()
    return
    

@app.post("/send-sms")
                        # is_store_data: str=Form(...)
def send(name: str=Form(...), email: str=Form(...), is_store_data: str=Form(...)):
    if verify_user(email)==True:
        return {"status":"Success", "det":f"Hey {name}, You are already a Subscriber\nPlease try with another E-mail"}
    else:
        otp = generate_otp()
        body=""
        if is_store_data=="TRUE":
            store_user(name, email)
            body = f"Hello {name},\nThank You for Subscribing to us.\nThis is your OTP: {otp}.\n\tTeam - Headline Hub"
        else:
            body = f"Hello {name},\nThis is your OTP: {otp}"
            
        try:
            msg = EmailMessage()
            msg.set_content(body)
            msg['subject']=otp
            msg['to']=email
            from_email = os.getenv("EMAIL")
            password = os.getenv("PASSWORD")
            
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(from_email, password)
            server.send_message(msg)
            server.quit()
            
            return {"status":"Success", "det":f"OTP successfully sent to {email}"}
        
        except Exception as e:
            return {"status":"Failed", "det":f"{HTTPException(status_code=500, detail=str(e))}"}


@app.post("/verify-otp")
def verify(otp: str=Form(...)):
    global otp_g
    if otp_g == otp:
        return {"status":"Success", "det":f"E-mail Verified Successfully"}
    else:
        return {"status":"Failed", "det":f"OTP Entered is not matched"}
    
