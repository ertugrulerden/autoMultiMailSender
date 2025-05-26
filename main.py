import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime
import os
import json
from time import sleep
import html

try:
    import streamlit as st
except ImportError:
    from os import system as osSystem
    osSystem("pip install streamlit")
    try:
        import streamlit as st
    except ImportError:
        raise ImportError("Failed to import streamlit even after installation.")


# https://myaccount.google.com/apppasswords
# create an "app" from the link and use the given code as app passwd

# default for gmail
DEFAULT_SMTP = "smtp.gmail.com"
DEFAULT_PORT = 465


SAVED_DATA_FILE = "saved_inputs.json"
SAVED_ATTACHMENTS_DIR = "saved_attachments"

def save_inputs(sender_email=None, sender_password=None, subject=None, body=None, recipients=None, smtp_settings=None, delay_hours=None, delay_minutes=None, delay_seconds=None, use_html=None):
    """Save input values to a JSON file, only updating the provided fields"""
    # Load existing data if file exists
    if os.path.exists(SAVED_DATA_FILE):
        with open(SAVED_DATA_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {
            "sender_email": "",
            "sender_password": "",
            "subject": "",
            "body": "",
            "recipients": "",
            "smtp_settings": {
                "smtp": DEFAULT_SMTP,
                "port": DEFAULT_PORT
            },
            "use_html": False,
            "delay_settings": {
                "hours": 0,
                "minutes": 0,
                "seconds": 0
            }
        }
    
    # Update only the provided fields
    if sender_email is not None:
        data["sender_email"] = sender_email
    if sender_password is not None:
        data["sender_password"] = sender_password
    if subject is not None:
        data["subject"] = subject
    if body is not None:
        data["body"] = body
    if recipients is not None:
        data["recipients"] = recipients
    if smtp_settings is not None:
        data["smtp_settings"] = smtp_settings
    if use_html is not None:
        data["use_html"] = use_html
    if any(x is not None for x in [delay_hours, delay_minutes, delay_seconds]):
        if "delay_settings" not in data:
            data["delay_settings"] = {}
        if delay_hours is not None:
            data["delay_settings"]["hours"] = delay_hours
        if delay_minutes is not None:
            data["delay_settings"]["minutes"] = delay_minutes
        if delay_seconds is not None:
            data["delay_settings"]["seconds"] = delay_seconds
    
    with open(SAVED_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_inputs():
    """Load saved input values from JSON file"""
    if not os.path.exists(SAVED_DATA_FILE):
        return None
    
    with open(SAVED_DATA_FILE, "r") as f:
        data = json.load(f)
    
    return data



col_icon, col_title = st.columns([1, 8])
with col_icon:
    st.image("icon.png", width=96)
with col_title:
    st.title("Auto Mail Sender")



if "sender_email" not in st.session_state:
    st.session_state.sender_email = ""
if "sender_password" not in st.session_state:
    st.session_state.sender_password = ""
if "subject" not in st.session_state:
    st.session_state.subject = ""
if "body" not in st.session_state:
    st.session_state.body = ""
if "recipients" not in st.session_state:
    st.session_state.recipients = ""
if "smtp" not in st.session_state:
    st.session_state.smtp = DEFAULT_SMTP
if "port" not in st.session_state:
    st.session_state.port = DEFAULT_PORT
if "emails_sent" not in st.session_state:
    st.session_state.emails_sent = 0
if "total_emails" not in st.session_state:
    st.session_state.total_emails = 0
if "hours" not in st.session_state:
    st.session_state.hours = 0
if "minutes" not in st.session_state:
    st.session_state.minutes = 0
if "seconds" not in st.session_state:
    st.session_state.seconds = 0
if "use_html" not in st.session_state:
    st.session_state.use_html = False


col1, col2 = st.columns([5, 3])


with col1:
    with st.expander("⚙️ SMTP Settings"):
        st.session_state.smtp = st.text_input("SMTP Server", value=st.session_state.smtp, on_change=lambda: on_input_change("smtp"))
        st.session_state.port = st.number_input("SMTP Port", value=st.session_state.port, step=1, on_change=lambda: on_input_change("port"))
        if st.button("Reset to Default"):
            st.session_state.smtp = DEFAULT_SMTP
            st.session_state.port = DEFAULT_PORT
            save_inputs(smtp_settings={"smtp": DEFAULT_SMTP, "port": DEFAULT_PORT})
            st.rerun()


with col2:
    if st.button("🔄 Recover Last Inputs", use_container_width=True):
        saved_data = load_inputs()
        if saved_data:
            st.session_state.sender_email = saved_data.get("sender_email", "")
            st.session_state.sender_password = saved_data.get("sender_password", "")
            st.session_state.subject = saved_data.get("subject", "")
            st.session_state.body = saved_data.get("body", "")
            st.session_state.recipients = saved_data.get("recipients", "")
            if "smtp_settings" in saved_data:
                st.session_state.smtp = saved_data["smtp_settings"].get("smtp", DEFAULT_SMTP)
                st.session_state.port = saved_data["smtp_settings"].get("port", DEFAULT_PORT)
            if "delay_settings" in saved_data:
                st.session_state.hours = saved_data["delay_settings"].get("hours", 0)
                st.session_state.minutes = saved_data["delay_settings"].get("minutes", 0)
                st.session_state.seconds = saved_data["delay_settings"].get("seconds", 0)
            st.session_state.use_html = saved_data.get("use_html", False)
            st.success("Inputs recovered successfully!")
        else:
            st.error("No saved inputs found!")

def on_input_change(field_name):
    """Handle input changes and save only the changed field"""
    if field_name == "sender_email":
        save_inputs(sender_email=st.session_state.sender_email)
    elif field_name == "sender_password":
        save_inputs(sender_password=st.session_state.sender_password)
    elif field_name == "subject":
        save_inputs(subject=st.session_state.subject)
    elif field_name == "body":
        save_inputs(body=st.session_state.body)
    elif field_name == "recipients":
        save_inputs(recipients=st.session_state.recipients)
    elif field_name == "smtp":
        save_inputs(smtp_settings={"smtp": st.session_state.smtp, "port": st.session_state.port})
    elif field_name == "port":
        save_inputs(smtp_settings={"smtp": st.session_state.smtp, "port": st.session_state.port})
    elif field_name == "hours":
        save_inputs(delay_hours=st.session_state.hours)
    elif field_name == "minutes":
        save_inputs(delay_minutes=st.session_state.minutes)
    elif field_name == "seconds":
        save_inputs(delay_seconds=st.session_state.seconds)
    elif field_name == "use_html":
        save_inputs(use_html=st.session_state.use_html)

sender_email = st.text_input("Your Email Address", value=st.session_state.sender_email, key="sender_email", on_change=lambda: on_input_change("sender_email"))
sender_password = st.text_input(
    "App Password", 
    value=st.session_state.sender_password, 
    type="password", 
    key="sender_password", 
    on_change=lambda: on_input_change("sender_password"),
    help="To get an app password for Gmail:\n1. Go to your Google Account settings\n2. Navigate to Security\n3. Enable 2-Step Verification if not already enabled\n4. Go to [THIS](https://myaccount.google.com/apppasswords) page\n5. Create an 'app', use the given code as password"
)

subject = st.text_input("Mail Subject", value=st.session_state.subject, key="subject", on_change=lambda: on_input_change("subject"))
use_html = st.toggle("Enable HTML Support", value=st.session_state.use_html, key="use_html", on_change=lambda: on_input_change("use_html"))
body = st.text_area("Mail Body", value=st.session_state.body, key="body", height=500, on_change=lambda: on_input_change("body"), 
                   help="You can use plain text or HTML (if enabled above) for your email body. For HTML, basic tags like <b>, <i>, <a>, etc. are supported.")
recipients = st.text_area("Recipient Emails (one per line)", value=st.session_state.recipients, key="recipients", on_change=lambda: on_input_change("recipients"), height=150)
attachments = st.file_uploader("Attachments", accept_multiple_files=True)
log_placeholder = st.empty()




def logToTxt(logfile, logtext):
    with open(logfile, "a") as f:
        now = datetime.datetime.now().strftime("%d/%m-%H:%M:%S")
        f.write(f"{now} \t|\t {logtext}\n")

def send_gmail(sender_email, sender_password, recipient_email, subject, body, attachments=None):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject


    if st.session_state.use_html:
        msg.attach(MIMEText(body, 'html'))
    else:
        msg.attach(MIMEText(body, 'plain'))

    if attachments:
        for uploaded_file in attachments:
            try:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(uploaded_file.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={uploaded_file.name}')
                msg.attach(part)
            except Exception as e:
                st.error(f"Failed to attach file: {uploaded_file.name}, error: {e}")
                logToTxt("log.txt", f"FAIL TO ATTACH: {uploaded_file.name} to {recipient_email} \t ERROR: {e}")

    try:
        with smtplib.SMTP_SSL(st.session_state.smtp, st.session_state.port) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        st.session_state.emails_sent += 1
        st.success(f"Email sent successfully to '{recipient_email}' ({st.session_state.emails_sent}/{st.session_state.total_emails})")
        logToTxt("log.txt", f"SENT: {recipient_email}")

    except Exception as e:
        st.error(f"Failed to send email: {e}")
        logToTxt("log.txt", f"FAIL: {recipient_email} \t ERROR: {e}")


colText, col1, col2, col3 = st.columns(4)
with colText:
    st.subheader("Delay")
    st.caption("Set a delay between sending each email.")
with col1:
    hours = st.number_input("Hours", key="hours", min_value=0, step=1, format="%d", on_change=lambda: on_input_change("hours"))
with col2:
    minutes = st.number_input("Minutes", key="minutes", min_value=0, step=1, format="%d", on_change=lambda: on_input_change("minutes"))
with col3:
    seconds = st.number_input("Seconds", key="seconds", min_value=0, step=1, format="%d", on_change=lambda: on_input_change("seconds"))



with st.container():
    with st.expander("Log Output", expanded=False):
        try:
            with open("log.txt", "r") as log_file:
                lines = log_file.readlines()
                logs = "".join(reversed(lines))
        except FileNotFoundError:
            st.warning("Log file not found.")
        
        st.text_area("Log File", logs, height=300)
        st.caption("This log shows the most recent email activity starting from top. Errors and successes are recorded here.")
    
        


    if st.button("📧 Send Emails", use_container_width=True):
        if not st.session_state.sender_email or not st.session_state.sender_password or not st.session_state.subject or not st.session_state.body or not st.session_state.recipients:
            st.error("Please fill in all fields.")
        else:
            recipient_list = [email.strip() for email in st.session_state.recipients.splitlines() if email.strip() and not email.strip().startswith("//")]
            st.session_state.total_emails = len(recipient_list)
            st.session_state.emails_sent = 0
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, mail in enumerate(recipient_list):
                send_gmail(
                    sender_email=st.session_state.sender_email,
                    sender_password=st.session_state.sender_password,
                    recipient_email=mail,
                    subject=st.session_state.subject,
                    body=st.session_state.body,
                    attachments=attachments if attachments else None
                )
                progress = (i + 1) / len(recipient_list)
                progress_bar.progress(progress)

                status_text.text(f"Progress: {i+1}/{st.session_state.total_emails} tried \t Success: {st.session_state.emails_sent} \t Failed: {(i+1) - st.session_state.emails_sent}")


                delayToUse = (hours*60*60)+(minutes*60)+seconds
                if (delayToUse > 0) and (i < len(recipient_list) - 1):
                    sleep(delayToUse)
                

            with open("log.txt", "a") as f:
                f.write("\n")
            st.info(f"All emails processed. {st.session_state.emails_sent}/{st.session_state.total_emails} emails sent successfully. Check Log Output for details.")

