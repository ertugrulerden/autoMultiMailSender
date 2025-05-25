import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime
import os
import json

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

def save_inputs(sender_email, sender_password, subject, body, recipients, smtp_settings):
    """Save all input values to a JSON file"""
    data = {
        "sender_email": sender_email,
        "sender_password": sender_password,
        "subject": subject,
        "body": body,
        "recipients": recipients,
        "smtp_settings": smtp_settings
    }
    
    with open(SAVED_DATA_FILE, "w") as f:
        json.dump(data, f)

def load_inputs():
    """Load saved input values from JSON file"""
    if not os.path.exists(SAVED_DATA_FILE):
        return None
    
    with open(SAVED_DATA_FILE, "r") as f:
        data = json.load(f)
    
    return data

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


col1, col2 = st.columns([3, 1])


with col1:
    with st.expander("⚙️ SMTP Settings"):
        st.session_state.smtp = st.text_input("SMTP Server", value=st.session_state.smtp)
        st.session_state.port = st.number_input("SMTP Port", value=st.session_state.port, step=1)
        if st.button("Reset to Default"):
            st.session_state.smtp = DEFAULT_SMTP
            st.session_state.port = DEFAULT_PORT
            st.rerun()


with col2:
    if st.button("Recover Last Inputs", use_container_width=True):
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
            st.success("Inputs recovered successfully!")
        else:
            st.error("No saved inputs found!")

def on_input_change():
    save_inputs(
        st.session_state.sender_email,
        st.session_state.sender_password,
        st.session_state.subject,
        st.session_state.body,
        st.session_state.recipients,
        {"smtp": st.session_state.smtp, "port": st.session_state.port}
    )

sender_email = st.text_input("Your Email Address", value=st.session_state.sender_email, key="sender_email", on_change=on_input_change)
sender_password = st.text_input("App Password", value=st.session_state.sender_password, type="password", key="sender_password", on_change=on_input_change)
subject = st.text_input("Mail Subject", value=st.session_state.subject, key="subject", on_change=on_input_change)
body = st.text_area("Mail Body", value=st.session_state.body, key="body", on_change=on_input_change)
recipients = st.text_area("Recipient Emails (one per line)", value=st.session_state.recipients, key="recipients", on_change=on_input_change, height=150)
attachments = st.file_uploader("Attachments", accept_multiple_files=True)

log_placeholder = st.empty()

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
        st.success(f"Email sent successfully to '{recipient_email}'")
        logToTxt("log.txt", f"SENT: {recipient_email}")

    except Exception as e:
        st.error(f"Failed to send email: {e}")
        logToTxt("log.txt", f"FAIL: {recipient_email} \t ERROR: {e}")

if st.button("Send Emails"):
    if not sender_email or not sender_password or not subject or not body or not recipients:
        st.error("Please fill in all fields.")
    else:
        recipient_list = [email.strip() for email in recipients.splitlines() if email.strip() and not email.strip().startswith("//")]
        for mail in recipient_list:
            send_gmail(
                sender_email=sender_email,
                sender_password=sender_password,
                recipient_email=mail,
                subject=subject,
                body=body,
                attachments=attachments if attachments else None
            )
        st.info("All emails processed. Check log.txt for details.")

