# Auto Mail Sender

A simple Python tool to send bulk emails with attachments through a user-friendly web interface.

## Quick Start

1. Install Python 3.x
2. Clone and run:
```bash
git clone https://github.com/ertugrulerden/autoMultiMailSender.git
cd autoMultiMailSender
pip install streamlit
streamlit run main.py
```

## Main Features

- Send emails to multiple recipients at once
- Add file attachments
- Set delays between emails
- Save your email settings
- Track email sending progress
- Works with Gmail (and other email providers)

## Gmail Setup

To use Gmail:
1. Enable 2-Step Verification in your Google Account
2. Create an App Password: [Google App Passwords](https://myaccount.google.com/apppasswords)
3. Use this password in the app

## Example Screenshot
<img width="555" alt="mailSs" src="https://github.com/user-attachments/assets/d60bdb95-de81-4486-b296-639c14504289" />


## License

MIT License - see LICENSE file for details.

---

## Detailed Features

### Email Features
- 📧 Send bulk emails to multiple recipients
- 📎 Support for multiple file attachments
- 🎨 HTML email support with toggle option
- 💬 Support for comments in recipient list (lines starting with //)

### Security & Settings
- 🔒 Secure SMTP connection with SSL
- ⚙️ Customizable SMTP settings
- 🔄 Default Gmail configuration with easy reset option
- 🔐 Secure password field for app password

### Automation & Timing
- ⏱️ Configurable delay between emails (hours, minutes, seconds)
- 🎲 Random delay variation between emails
- ⏳ Countdown timer for delays between emails

### User Experience
- 💾 Auto-save form inputs for quick recovery
- 📱 Responsive layout with column-based design
- 💡 Helpful tooltips for complex features
- 🎯 Auto-installation of required dependencies

### Monitoring & Logging
- 📊 Real-time progress tracking with success/failure counts
- 📈 Progress bar visualization
- 🔍 Detailed status display showing attempted, successful, and failed emails
- 📋 Expandable log output section
- 📝 Detailed logging of email operations
