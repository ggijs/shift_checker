import email_handeling
import data_handeling
import credentials
import time

class Shift_checker:

    def __init__(self):
        self.pwd = credentials.get_pwd()
        self.email_addr = credentials.get_email()
        self.email_client = email_handeling.Email(self.email_addr, self.pwd)
        self.checker = data_handeling.Checker()
        self.input_list = []
        self.output_list = []

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

    def run(self):
        #run entire process then wait for 60 seconds
        self.update_input()
        self.process_input()
        self.return_output()
        time.sleep(60)