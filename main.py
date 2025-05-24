import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime


# https://myaccount.google.com/apppasswords
# create an "app" from the link and use the given code as mailAppPass

yourMail = "yourmail@ordek.com"
mailAppPass = "xxxx xxxx xxxx xxxx"

# example inputs
mailTitle = "International Internship - Ordek"
mailBody = """
Dear mr or mrs.

I hope this message finds you well. My name is Ordek, and I am a first-year Software Engineering student at X University. I am writing to express my interest in an internship opportunity at your institution.

I'm eager to contribute and grow in areas such as software development and computer science. You'll find my CV and Motivation letter attached for your review.

Thank you for your time and consideration.

Best regards,
Ordek
"""

attachmentsToAdd = [
    "egCV.pdf",
    "egMotivLet.pdf",
]



def logToTxt(logfile, logtext):
    with open(logfile, "a") as f:
        now = datetime.datetime.now().strftime("%d/%m-%H:%M:%S")
        f.write(f"{now}\t|\t{logtext}\n")

def send_gmail(sender_email, sender_password, recipient_email, subject, body, attachments=None):
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    if attachments:
        for filename in attachments:
            try:
                with open(filename, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={filename}')
                msg.attach(part)

            except Exception as e:
                print(f"Failed to attach file: {filename}, error: {e}")
                logToTxt("log.txt", f"FAIL TO ATTACH: {filename} to {recipient_email} \t ERROR: {e}")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print(f"Email sent successfully to '{recipient_email}'")
        logToTxt("log.txt", f"SENT: {recipient_email}")

    except Exception as e:
        print(f"Failed to send email: {e}")
        logToTxt("log.txt", f"FAIL: {recipient_email} \t ERROR: {e}")



with open("mails.txt", "r") as f:
    for line in f:
        line = line.replace(" ", "").replace("\t", "").strip()
        if ("//" in line) or line=="":
            continue
        mail = line

        send_gmail(
            sender_email=yourMail,
            sender_password=mailAppPass,
            recipient_email=mail,
            subject=mailTitle,
            body=mailBody,
            attachments=attachmentsToAdd
        )
    
    with open("log.txt", "a") as f:
        f.write(f"\n")

