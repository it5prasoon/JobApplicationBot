from smtplib import SMTP
from email.encoders import encode_base64
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import environ as os_environ

def send_email(email_receiver, subject, email_body):
    fromaddr = "login.docplus@gmail.com"              #USE YOUR EMAIL ID HERE
    toaddr = email_receiver
    
    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = subject

    # string to store the body of the mail
    body = email_body

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = "Resume.docx"
    #attachment = open(f"{pathlib.Path(__file__).parent.resolve()}\Manish Kothary -Chief Technology Officer Resume.DOCX", "rb")
    attachment = open(f"Manish Kothary -Chief Technology Officer Resume.DOCX", "rb")
    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    password=os_environ.get("GMAIL_APP_PASSWORD")
    
    s.login(fromaddr, password)       #USE YOUR OWN APP PASSWORD; DIFFERENT FROM YOUR GMAIL PASSOWRD

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)
    print('A MAIL HAS BEEN SENT')
    # terminating the session
    s.quit()
