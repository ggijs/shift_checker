import csv

class Data:

    def __init__(self, file, sender):
        self.input = file
        self.output = ''
        self.sender = sender
        self.header = self.check_for_header()
        self.header_layout = self.set_header_layout()
        self.invalid_file_layout = False

    def check_for_header(self):
        with open(self.input) as f:
            return csv.Sniffer().has_header(f.read())

    def set_header_layout(self):
        if self.header:
            layout = {}
            with open(self.input, encoding='utf-8-sig') as f:
                f = next(csv.reader(f, delimiter=';'))
                for i in range(len(f)):
                    layout[f[i].lower()] = i
            return layout
        else:
            print('No header layout found')

    def get_data(self):
        return self.input

    def get_header_layout(self):
        return self.header_layout

    def set_output_file(self, filename):
        self.output =  filename

    def set_invalid_file_layout(self):
        self.invalid_file_layout = True