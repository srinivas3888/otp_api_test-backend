from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import smtplib
from email.message import EmailMessage
import random
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
def generate_otp() -> str:
    global otp_g
    otp_g = str( random.randrange(1000, 9999) )
    return otp_g
    
@app.post("/send-sms")
def send(name: str=Form(...), email: str=Form(...), check: str=Form(...)):
    body=""
    otp=""
    if check=="0":
        otp = generate_otp()
        body = f"Hello {name},\nThank You for Subscribing to us.\nThis is your OTP: {otp}.\n\tTeam - Headline Hub"
        
    elif check=="1":
        otp="1"
        msg['subject']="Registration Successful || Guardian-Sphere"
        body = f"Hello {name},\nThank you for Registration.\t Your all set \n\t - Guardian-Sphere"
        
    else:
        custom_msg: str=Form(...)               # custom msg
        body = f"Hello {name},\n{custom_msg}\n\tTeam - ZARTEX"
        
    try:
        msg = EmailMessage()
        msg.set_content(body)
        if otp=="":
            custom_sub: str=Form(...)           # custom subject
            msg['subject']=custom_sub
        else:
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



# Testing / Ping...
@app.get("/test")
def hello():
    try:
        return {"Success":"API is live."}
    except Exception as e:
        return {"Failed":str(e)}
