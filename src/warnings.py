import smtplib
from email.message import EmailMessage
from constants import *
import json

msg = EmailMessage()
msg["Subject"] = "Youtube Uploader Ran"
msg["From"] = "m07wang@gmail.com"
msg["To"] = "m07wang@gmail.com"

msg.set_content("The Youtube uploader ran again.")

with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
    with open(SECRETS_FILE, "w") as f:
        data = json.load(f)
        email = data["gmail-login"]["email"]
        password = data["gmail-login"]["password"]
 
        smtp.starttls()
        smtp.login(email, password)
        smtp.send_message(msg)