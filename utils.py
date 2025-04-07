import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import cred

async def send_email(
        recipient_email,
        body,
        sender_email= cred["senderEmail"],
        sender_password=cred["senderPassword"],
        subject="OTP FOR LOGIN"):
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        # Correct SMTP server and port
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)

        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)

        print(f"\nEmail sent to {recipient_email}\n")
        server.quit()
    except Exception as e:
        print("Failed to send mail")
        print(e)

if __name__ == "__main__":
    recipient_mail = "artiarorasingh@gmail.com"
    body = "Testing"
    send_email(recipient_email=recipient_mail, body=body)
