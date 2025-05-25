import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime


# https://myaccount.google.com/apppasswords
# create an "app" from the link and use the given code as mailAppPass

with open("mailAndPass.txt", "r") as f:
    lines = [line.strip() for line in f if line.strip()]
    yourMail = lines[0]
    mailAppPass = lines[1]

with open("mailTitle.txt", "r", encoding="utf-8") as f:
    mailTitle = f.read().strip()

with open("mailBody.txt", "r", encoding="utf-8") as f:
    mailBody = f.read().strip()

attachmentsToAdd = [
    "egCV.pdf",
    "egMotivLet.pdf",
]

# for gmail
SMTP = "smtp.gmail.com"
PORT = 465 




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
        with smtplib.SMTP_SSL(SMTP, PORT) as server:
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

