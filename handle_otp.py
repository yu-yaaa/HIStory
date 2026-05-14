import smtplib
import random
import string
import os
import time
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from queries import save_otp
load_dotenv()

email = os.getenv("EMAIL_ADDRESS")
password = os.getenv("EMAIL_PASSWORD")

otp_store = {"code": None, "expires_at": None}

def generate_otp(length=6):
    otp = ''.join(random.choices(string.digits, k=length))
    return otp

def send_email(receiver_email):
    otp = generate_otp()
    otp_store["code"] = otp
    otp_store["expires_at"] = time.time() + 300

    subject = "HIStory - Your Password Reset OTP"
    body = f"""
    Hello!
    
    Your OTP code for resetting your password is:

            {otp}

    This code expires in 5 minutes.
    Do not share this code with anyone.

    - HIStory Team
    """

    # Build the email
    msg = MIMEMultipart()
    msg["From"] = email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Connect to Gmail and send
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(email, password)
            server.sendmail(email, receiver_email, msg.as_string())
            save_otp(otp)
        print("OTP sent successfully!")
        return True

    except smtplib.SMTPAuthenticationError:
        print("ERROR: Wrong email or app password in .env!")
        return False

    except Exception as e:
        print(f"ERROR: Could not send email — {e}")
        return False
    
