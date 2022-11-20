import smtplib
import email.encoders
import email.mime.base
import email.mime.multipart
import email.mime.text

class Sender:

    def __init__(self, mailserver, emailaddr, pwd):
        self.PORT = 587
        self.mailserver = mailserver
        self.emailaddr = emailaddr
        self.pwd = pwd
        self.mail_data = None

    def create_message(self):
        message = email.mime.multipart.MIMEMultipart()
        message['From'] = self.emailaddr
        message['To'] = self.mail_data.sender

        if self.mail_data.invalid_file_layout:
            message.attach(email.mime.text.MIMEText('Er lijkt iets mis te zijn gegaan...', 'plain'))
        else:
            with open(self.mail_data.output, 'rb') as attachment:
                part = email.mime.base.MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                email.encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={self.mail_data.output}')
                message.attach(part)
        return message.as_string() 

    def send_mail(self, data):
        self.mail_data = data
        message =  self.create_message()

        connection = smtplib.SMTP(self.mailserver, self.PORT)
        connection.starttls()
        connection.login(self.emailaddr, self.pwd)

        connection.sendmail(self.emailaddr, self.mail_data.sender, message)
        print(f'reply send to {self.mail_data.sender}')

        connection.quit()