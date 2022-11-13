import imaplib
import email
import email.utils
import data

class Receiver:

    def __init__(self, mailserver, emailaddr, pwd):
        self.mailserver = mailserver
        self.emailaddr = emailaddr
        self.pwd = pwd
        self.mails = []
        self.PORT = 993
        
    def connect(self):
        mailbox = imaplib.IMAP4_SSL(self.mailserver, self.PORT)
        mailbox.login(self.emailaddr, self.pwd)
        mailbox.select()
        return mailbox

    def disconnect(self, mailbox):
        mailbox.close()
        mailbox.logout()

    def get_mails(self):
        mailbox = self.connect()
        r, msglist = mailbox.search(None, 'UNSEEN')
        if r == 'OK':
            for msg in msglist[0].split():
                r, data = mailbox.fetch(msg, '(RFC822)')
                self.mails.append(email.message_from_bytes(data[0][1]))
        print(f'found {len(self.mails)} new emails')
        self.disconnect(mailbox)

    def save_attachements(self, msg):
        attachment_list = []
        for part in msg.walk():
            if part.get_content_type() == 'multipart':
                continue
            if part.get_content_disposition() == None:
                continue
            filename =  part.get_filename()
            if not self.check_extension(filename, '.csv'):
                continue
            attachment_list.append(filename)
            with open(filename, 'wb') as f:
                f.write(part.get_payload(decode=True))
        return attachment_list

    def get_sender(self, msg):
        return email.utils.parseaddr(msg.get('From'))[1]

    def check_extension(self, filename, extension):
        if filename[-len(extension):] == extension:
            return True
        else:
            return False

    def save_all_csv(self):
        self.mails = []
        data_files = []
        self.get_mails()
        for mail in self.mails:
            attachment_list = self.save_attachements(mail)
            sender = self.get_sender(mail)
            for attachment in attachment_list:
                data_files.append(data.Data(attachment, sender))
        print(f'found {len(data_files)} new csv files')
        return data_files