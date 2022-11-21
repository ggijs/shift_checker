import email_handeling
import data_handeling
import credentials
import time
from socket import gaierror

class Shift_checker:

    def __init__(self):
        self.pwd = credentials.get_pwd()
        self.email_addr = credentials.get_email()
        self.email_client = email_handeling.Email(self.email_addr, self.pwd)
        self.checker = data_handeling.Checker()
        self.input_list = []
        self.output_list = []
        self.cleanup_list = []

    def update_input(self):
        #add all new csv files to input list
        files = self.email_client.get_data()
        if files != None:
            print(f'Adding {len(files)} files')
            for f in files:
                self.input_list.append(f)

    def process_input(self):
        #removes data object from input list, create output file, adds to output list
        while len(self.input_list) > 0:
            input = self.input_list.pop()
            self.output_list.append(self.checker.process(input))

    def return_output(self):
        while len(self.output_list) > 0:
            output = self.output_list.pop()
            self.email_client.sender.send_mail(output)
            self.cleanup_list.append(output)

    def clean_up(self):
        while len(self.cleanup_list) > 0:
            data = self.cleanup_list.pop()
            data.delete_files()
        self.email_client.delete_read()

    def run(self):
        #run entire process then wait for 60 seconds
        try:
            self.update_input()
        except gaierror:
            #added to deal with DNS problem
            print('Cannot connect to mailserver')
        self.process_input()
        self.return_output()
        self.clean_up()
        time.sleep(60)