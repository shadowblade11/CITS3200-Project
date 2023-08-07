import random
import string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def generate_v_code(length = 6):  #generate 6 digits verification codes
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def send_v_code(email_addr, v_code):
    smtp_server = 'smtp.Gmail.com'
    smtp_port = 587
    sender = "xiaojunh6@gmail.com"
    sender_password = "gddehhtyhlpzhhpn"

    subject = "Verification Code for Italian Oral Presentation Skill"
    message = f"Your verification code is : {v_code}"

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = email_addr
    msg['Subject'] = subject
    msg.attach(MIMEText(message,'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender,sender_password)
        server.sendmail(sender,email_addr,msg.as_string())
        server.quit()
        print("send successfully")
    except Exception as e:
        print("Error: ", str(e))


# send_v_code("23011392@student.uwa.edu.au")