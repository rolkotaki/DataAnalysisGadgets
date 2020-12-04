import csv
from datetime import datetime
from collections import namedtuple


# https://docs.python.org/3/library/csv.html


# ********** Reading and writing files

def read_write_file(file_name, new_file_name):
    """This proceudre read the content of a file and writes it into another file."""
    file = open(file_name, 'rt', encoding='utf8')  # rt - read and text mode; this is by default
    print(file.read())      # reading the whole content of the file
    file.seek(0)            # going back to the beginning of the file
    print(file.readline())  # reading one line
    print(file.readline())  # reading one line, the next one
    file.seek(0)
    print(file.read(5))     # reading 5 bytes
    file.seek(0)
    for line in file:       # looping throught the files
        print(line)
    file.seek(0)
    for line in file.readlines():  # readlines() returns a list whose each element is a line of the file
        print(line)

    new_file = open(new_file_name, 'wt', encoding='utf8')
    new_file.write('I am the first line ...\n')
    new_file.writelines(['First item of the list of lines\n', 'Second  no new line ', 'Third\n'])

    for line in open(file_name, 'rt', encoding='utf8'):
        new_file.write(line)
    new_file.writelines(open(file_name, 'rt', encoding='utf8').readlines())

    new_file.close()

    new_file = open(new_file_name, 'a+')  # we open the file again, but in append mode (to the end)
    new_file.write('I am appended to the end of the file ...\n')
    new_file.close()


# ********** Reading and writing CSV files - with csv reader and writer

def read_write_csv(file_name, new_file_name):
    """This procedure reads a csv and writes the content into another file.
    We use the basic reader and writer object.
    """
    file = open(file_name, 'r', newline='', encoding='utf8')
    csv_reader = csv.reader(file, delimiter=',')  # a reader object which will iterate over lines in the given csv file

    new_file = open(new_file_name, 'w', newline='', encoding='utf8')
    # a writer object responsible for converting the user’s data into delimited strings on the given file-like object
    csv_writer = csv.writer(new_file, delimiter=',')

    for line in csv_reader:
        csv_writer.writerow(line)
        # print(line)

    new_file.close()


# ********** Reading CSV file with validation and writing - using DictReader and DictWriter and a generator function

# a named tuple for original column name, mapped column name and data type
Column = namedtuple('Column', 'src dest convert')


def parse_timestamp(text):
    """This function parses a string to datetime."""
    return datetime.strptime(text, '%Y-%m-%d %H:%M:%S')


# We will not load all columns from the file, only some of them. The below list contains named tuple objects for
# all the columns that we want to import. The named tuple object contains the mapped column name and data type.
columns = [
    Column('VendorID', 'vendor_id', int),
    Column('passenger_count', 'num_passengers', int),
    Column('tip_amount', 'tip', float),
    Column('total_amount', 'price', float),
    Column('tpep_dropoff_datetime', 'dropoff_time', parse_timestamp),
    Column('tpep_pickup_datetime', 'pickup_time', parse_timestamp),
    Column('trip_distance', 'distance', float),
]


def iter_records(file_name):
    """We load the file, loop through the lines (loaded as dictionaries) and return them one-by-one (yield).
    We use DictReader.
    This procedure is a generator that is used to iterate through the file."""
    # info: https://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do
    with open(file_name, 'rt', newline='') as fp:
        # DictReader: an object that operates like a regular reader, but maps the information in each row to a dict
        # whose keys are given by the optional fieldnames parameter:
        reader = csv.DictReader(fp)
        for csv_record in reader:
            record = {}
            for col in columns:  # we loop through the columns and convert the values to the correct data types
                value = csv_record[col.src]
                record[col.dest] = col.convert(value)
            yield record


def write_csv_by_dict(file_name, new_file_name):
    """We loop through the records (dictionaries) returned by iter_records and write them into a new file.
    We use DictWriter.
    """
    new_file = open(new_file_name, 'wt', newline='')
    fieldnames = [col.dest for col in columns]
    # an object which operates like a regular writer but maps dictionaries onto output rows
    writer = csv.DictWriter(new_file, fieldnames=fieldnames)
    writer.writeheader()
    file_content = []
    for record in iter_records(file_name):
        # writer.writerow(record)  # this way we would write the lines into the file line by line
        file_content.append(record)
    writer.writerows(file_content)  # here we create a list of dictionaries and write the content into the file at once
    new_file.close()


def read_with_validate_and_write(file_name, new_file_name):
    """We read the file content and write it into another file, keeping only some columns"""
    write_csv_by_dict(file_name, new_file_name)


if __name__ == "__main__":
    read_write_file('../data/text.txt', '../data/text_new.txt')
    read_write_csv('../data/olympics.csv', '../data/olympics_new.csv')
    read_with_validate_and_write('../data/taxi.csv', '../data/taxi_new.csv')
