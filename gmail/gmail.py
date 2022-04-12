import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv


class Gmail:
    def __init__(self):
        load_dotenv()
        self.sender = os.getenv("GMAIL_USER")
        self.sender_name = os.getenv("GMAIL_SENDER_NAME")
        self.pw = os.getenv("GMAIL_PW")

    def send_email(self, recipient, text, subject):
        # Setup stuff
        message = self.setup_message(recipient, text, subject)
        session = self.create_session()

        # Send the email
        try:
            session.sendmail(self.sender, recipient, message)

        except Exception as e:
            print(e)
            return "Email Error"

        session.quit()
        print("Email sent successfully")
        return "Success"

    def setup_message(self, recipient, text, subject):
        message = MIMEMultipart()
        message["From"] = self.sender_name
        message["To"] = recipient
        message["Subject"] = subject
        message.attach(MIMEText(text, "plain"))
        return message.as_string()

    def create_session(self):
        session = smtplib.SMTP("smtp.gmail.com", 587)
        session.starttls()
        session.login(self.sender, self.pw)
        return session
