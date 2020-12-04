import pandas as pd
import numpy as np


# ********** Reading CSV into pandas dataframe

# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html

df1 = pd.read_csv('../data/taxi.zip', skiprows=1, skip_blank_lines=True,  delimiter=',', warn_bad_lines=True,
                  header=None,  # None = custom headers by names; 0 = headers from line; otherwise the row number
                  names=['vendor_id', 'tpep_pickup_datetime', 'tpep_dropoff_datetime', 'passenger_count',
                         'trip_distance', 'ratecode_id', 'store_and_fwd_flag', 'PULocationID', 'DOLocationID',
                         'payment_type', 'fare_amount', 'extra', 'mta_tax', 'tip_amount', 'tolls_amount',
                         'improvement_surcharge', 'total_amount'],
                  compression='zip'  # it will decompress the file automatically (it must contain only one datafile)
                  )

df2 = pd.read_csv('../data/taxi.csv', skip_blank_lines=True,  delimiter=',', decimal='.', encoding='utf8',
                  header=0,  # first line contains the headers
                  index_col=['VendorID', 'tpep_pickup_datetime'],  # we specify the index column(s)
                  usecols=['VendorID', 'passenger_count', 'tip_amount', 'total_amount', 'tpep_dropoff_datetime',
                           'tpep_pickup_datetime', 'trip_distance'],  # only to load these columns; col index list too
                  dtype={'VendorID': np.int32, 'passenger_count': int, 'tip_amount': np.float64,
                         'total_amount': np.float64, 'tpep_dropoff_datetime': object,
                         'tpep_pickup_datetime': object, 'trip_distance': float},  # date can be object, will be parsed
                  parse_dates=['tpep_pickup_datetime', 'tpep_dropoff_datetime']
                  # date_parser=our own parser function, otherwise automatic
                  )

print(df1.dtypes)
print(df2.dtypes)  # here dates are datetime objects

print(df1.index)   # default integer index
print(df2.index)   # vendor id and pickup date are the index columns

print(df1.head())
print(df2.head())  # here we have less columns, only the ones we specified


# ********** Saving data from dataframe to csv

# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html

df2.to_csv(path_or_buf='../data/exported_df.csv', sep=',', decimal='.', mode='w', encoding='utf8',
           index_label=False,  # so that it is not included in the header label list
           header=['VENDORID', 'TPEP_PICKUP_DATETIME', 'TRIP_DISTANCE', 'TIP_AMOUNT', 'TOTAL_AMOUNT'],
           compression=None,
           line_terminator=None, date_format='%Y-%m-%d %H:%M:%S',
           chunksize=1000
           )

df2.to_csv(path_or_buf='../data/exported_df.zip', sep=',', decimal='.', mode='w', encoding='utf8',
           index=True, header=True,  # they are True by default also
           compression={'method': 'zip', 'archive_name': 'df2.csv'},  # the compression method and archive name
           date_format='%Y-%m-%d %H:%M:%S'
           )


# ********** Using chunksize for huge data

# https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-chunking
# https://maxhalford.github.io/blog/pandas-streaming-groupby/

df_reader = pd.read_csv('../data/taxi.csv', header=0, parse_dates=['tpep_pickup_datetime', 'tpep_dropoff_datetime'],
                        chunksize=1000)
# The returned object is NOT a dataframe, but an iterable TextFileReader object.

for chunk in df_reader:
    print(len(chunk))  # the number of rows in each chunk (we have 10 000 rows, so we have 10 times 1000 rows)

# It is memory-efficient, but it is not as "easy" as with a single dataframe to perform operations such as groupby().


# ********** There are simple ways to read Excel, JSON and other files also:
# pd.read_excel()
# pd.read_json()
