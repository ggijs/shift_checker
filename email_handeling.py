import imaplib, smtplib, receiver

class Email:

    def __init__(self, email_addr, pwd):
        self.mailserver = 'smtp.office365.com'
        self.smtp_port = 587
        self.imap_port = 993
        self.mail_adress = email_addr
        self.pwd = pwd
        self.receiver = receiver.Receiver(self.mailserver, self.mail_adress, self.pwd)

    def delete_read(self):
        #deletes al read mail in mailbox
        with imaplib.IMAP4_SSL(self.mailserver, self.imap_port) as mail:
            mail.login(self.mail_adress, self.pwd)
            mail.select()
            r, msglist = mail.search(None, 'SEEN')
            for msg in msglist[0].split():
                mail.store(msg, "+FLAGS", "\\Deleted")
            mail.expunge()

    def new_mail(self):
        #returns true if unread mail is in mailbox
        with imaplib.IMAP4_SSL(self.mailserver, self.imap_port) as mail:
            mail.login(self.mail_adress, self.pwd)
            mail.select()
            r, msglist = mail.search(None, 'UNSEEN')
            if len(msglist[0]) > 0:
                return True

    def get_data(self):
        #returns a list with data objects containing new csv files from mails and sender email adress
        if self.new_mail():
            data = self.receiver.save_all_csv()
            return data