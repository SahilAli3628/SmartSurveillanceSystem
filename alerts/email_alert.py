import smtplib
from email.message import EmailMessage

def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user = "stunner.hustle@gmail.com"
    msg['from'] = user
    password = "gsilrkisquwemajr"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(user, password)
    server.send_message(msg)

    server.quit()

if __name__ == '__main__':
    email_alert("INTRUDER ALERT!!!", "We have detected strangers", "sahilali3628@gmail.com")
