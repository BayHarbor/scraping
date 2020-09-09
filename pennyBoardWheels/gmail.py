import smtplib
from config import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# The mail addresses and password
sender_address = config.sender_address
sender_pass = config.gmail_pass
receiver_address = config.receiver_address

# Setup the MIME
message = MIMEMultipart()
message['From'] = sender_address
message['To'] = receiver_address
message['Subject'] = 'Penny Board Wheels in Stock!'


def send_the_email(mail_content):
    # The body and the attachments for the mail
    message.attach(MIMEText(str(mail_content).strip('[]'), 'plain'))

    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()

    print('Mail Sent')
    # https://myaccount.google.com/lesssecureapps
