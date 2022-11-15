import csv
import datetime

class Checker:

    def __init__(self):
        self.shift_sheet = 'diensten.csv'
        self.shift_layout = self.set_shift_layout()
        self.time_sheet = self.set_time_sheet()
        self.data = None
        self.data_list = []

    def set_shift_layout(self):
        #returns a dict containing the header layout of the csv file with shift information
        layout = {}
        with open(self.shift_sheet, encoding='utf-8-sig') as f:
            f = next(csv.reader(f, delimiter=';'))
            for i in range(len(f)):
                layout[f[i].lower()] = i
        return layout

    def set_time_sheet(self):
        #returns a dict with lowercase shiftname and shift duration in hours as a float 
        sheet = {}
        with open(self.shift_sheet) as f:
            next(f)
            for i in csv.reader(f, delimiter=';'):
                sheet[i[self.shift_layout['dienst']].lower()] = self.calc_shift_hours(i[self.shift_layout['starttijd']], i[self.shift_layout['eindtijd']])
        return sheet

    def calc_shift_hours(self, start_time, end_time):
        #returns time difference from to strings as a float
        start_time = datetime.datetime.strptime(start_time, '%H:%M')
        end_time = datetime.datetime.strptime(end_time, '%H:%M')
        if start_time > end_time:
            delta = start_time - end_time
            return (24 - (delta.total_seconds()/(60*60)))
        else:
            delta = end_time - start_time
            return delta.total_seconds()/(60*60)

    def process(self, data):
        #creates output file and returns data object with added output
        self.data = data
        self.data_list = self.read_data()
        try:
            self.compare()
        except KeyError:
            print('Invalid file layout')
            self.data.set_invalid_file_layout()
            return self.data
        self.data_list[0][5] = 'Opmerkingen'
        self.remove_column(5)
        self.data_list = self.sort_list(self.data_list)
        output_filename = self.create_filename()
        self.data.set_output_file(output_filename)
        self.write_output(output_filename)
        return self.data

    def read_data(self):
        #returns the input csv file as a list
        file = []
        with open(self.data.get_data(), encoding='utf-8-sig') as d:
            for i in csv.reader(d, delimiter=';'):
                file.append(i)
        return file

    def compare(self):
        data_layout = self.data.get_header_layout()
        self.data_list = self.read_data()
        for i in self.data_list[1:]:
            (i[data_layout['uren']]) = float((i[data_layout['uren']]).replace(',','.'))
        for i in self.data_list[1:]:
            if (i[data_layout['uren']]) != self.time_sheet[i[data_layout['diensten']].lower()]:
                i.append('Aangepaste tijd')
    
    def remove_column(self, col):
        for i in self.data_list[1:]:
            del(i[col])

    def sort_list(self, list):
            list = list
            header = list[0]
            del(list[0])
            list.sort(key= lambda x: (x[1],x[0]))
            list.insert(0, header)
            return list

    def create_filename(self):
        #returns a output filename based on the date of the first data entry in the csv file
        months = {1 : 'januari',
                  2 : 'februari',
                  3 : 'maart',
                  4 : 'april',
                  5 : 'mei',
                  6 : 'juni',
                  7 : 'juli',
                  8 : 'augustus',
                  9 : 'september',
                  10 : 'oktober',
                  11 : 'november',
                  12 : 'december'}
        date = datetime.datetime.strptime(self.data_list[1][0], '%d-%m-%Y').date()
        month = date.month
        year = date.year
        filename = f'Aanvraag {months[month]} {year}.xls'
        return filename
    
    def write_output(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile,delimiter=',',dialect='excel')
            for i in self.data_list:
                writer.writerow(i)