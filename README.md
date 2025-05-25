# Auto Mail Sender

A Python-based email automation tool built with Streamlit that allows you to send bulk emails with attachments through a user-friendly web interface.

## Features

- 📧 Send bulk emails to multiple recipients
- 📎 Support for multiple file attachments
- 🔒 Secure SMTP connection with SSL
- 💾 Auto-save form inputs for quick recovery
- 📝 Detailed logging of email operations
- ⚙️ Customizable SMTP settings
- 🔄 Default Gmail configuration with easy reset option

## Prerequisites

- Python 3.x
- Gmail account (for default configuration)
- App password for Gmail (if using Gmail)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ertugrulerden/autoMultiMailSender.git
cd autoMultiMailSender
```

2. Install the required dependencies:
```bash
pip install streamlit
```

## Usage

1. Run the application:
```bash
streamlit run main.py
```

2. Open your web browser and navigate to the provided local URL (typically http://localhost:8501)

3. Configure your email settings:
   - Enter your email address
   - For Gmail users, use an App Password (see below)
   - Customize SMTP settings if needed
   - Enter email subject and body
   - Add recipient email addresses (one per line)
   - Upload any attachments if needed

4. Click "Send Emails" to start the sending process

## Gmail App Password Setup

To use Gmail as your SMTP server:

1. Go to your Google Account settings
2. Navigate to Security
3. Enable 2-Step Verification if not already enabled
4. Go to [App Passwords](https://myaccount.google.com/apppasswords)
5. Create a new app and use the generated password

## File Structure

- `main.py` - Main application file
- `saved_inputs.json` - Stores form inputs for recovery
- `log.txt` - Contains email sending logs
- `saved_attachments/` - Directory for saved attachments

## Logging

The application maintains a detailed log file (`log.txt`) that records:
- Successful email deliveries
- Failed attempts
- Attachment errors
- Timestamps for all operations

## Example Screenshot
<img width="720" alt="Screenshot 2025-05-25 at 16 16 50" src="https://github.com/user-attachments/assets/e702ccba-5440-4ff4-822d-1ad7e0044ea9" />

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
