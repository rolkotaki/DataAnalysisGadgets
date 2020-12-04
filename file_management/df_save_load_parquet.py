import pyarrow.parquet as pq
import pyarrow as pa
import pandas as pd


# https://arrow.apache.org/docs/python/parquet.html
# https://arrow.apache.org/docs/python/generated/pyarrow.parquet.read_table.html
# https://arrow.apache.org/docs/python/generated/pyarrow.Table.html (to_pandas(), from_pandas() and others)
# https://arrow.apache.org/docs/python/pandas.html
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.astype.html
# https://arrow.apache.org/docs/python/generated/pyarrow.parquet.write_table.html
# https://arrow.apache.org/docs/python/generated/pyarrow.Table.html#pyarrow.Table.from_pandas
# https://arrow.apache.org/docs/python/generated/pyarrow.parquet.ParquetFile.html#pyarrow.parquet.ParquetFile
# https://arrow.apache.org/docs/python/generated/pyarrow.parquet.ParquetWriter.html
# https://arrow.apache.org/docs/python/generated/pyarrow.parquet.ParquetDataset.html#pyarrow.parquet.ParquetDataset


# ********** Reading data from a parquet file

# Simplest way
print('Simple way of loading')

opfcp_parquet = pq.read_table('../data/opfcp.parquet')  # loading the parquet file into a pyarrow.Table object
opfcp = opfcp_parquet.to_pandas()                       # converting the pyarrow table into a pandas dataframe

del opfcp_parquet  # it is a good practice to delete this from the memory, we will not need it anymore

print(opfcp.head())
print(opfcp.dtypes)

# When reading a subset of columns from a file that used a Pandas dataframe as the source, we use read_pandas to
# maintain any additional index column data:
opfcp_parquet = pq.read_pandas('../data/opfcp.parquet', columns=['c_ean', 'price'])  #
opfcp = opfcp_parquet.to_pandas()

print(opfcp.head())
print(opfcp.dtypes)


# Using more parameters to load a file in a more custom way
print('Customized way of loading')

opfcp_parquet = pq.read_table('../data/opfcp.parquet',
                              # only some columns; if we provide a non-existing column name, it is simply ignored
                              columns=['c_mag', 'c_ean', 'price', 'c_promo', 'm_promo_price'],
                              use_pandas_metadata=False,  # it is useful if we have pandas metadata in the file
                              # use_legacy_dataset=False,
                              filters=None  # could be used to filer for partitions ???
                              )


def check_pa_dtype(a):
    """This is a test function that I passed as the types_mapper function to to_pandas(),
    to print out and see the data types coming from pyarrow.
    Originally to_pandas()'s types_mapper expects a dictionary's get function.
    """
    if a == pa.string():
        print('string')
    elif a == pa.int64():
        print('int64')
    elif a == pa.float32():
        print('float32')
    elif a == pa.float64():
        print('float64')
    else:
        print(a)


type_mappings = {pa.int64(): 'int64', pa.string(): str}

opfcp = opfcp_parquet.to_pandas(# ignore_metadata=False,
                                # If True, ‘pandas’ metadata is not used to reconstruct the DataFrame index, if present
                                # bool_self_destruct=True,
                                # bool_date_as_object=True,
                                # true: deallocates the originating memory as it is being converted to pandas dataframe
                                # types_mapper=check_pa_dtype  # types_mapper=type_mappings.get
                                # to map pyarrow data types to pandas data types
                                )

print(opfcp.head())
print(opfcp.dtypes)

# changing the data type in pandas (it may be late already)
opfcp = opfcp.astype({'price': 'float64', 'c_ean': 'int32', 'c_mag': 'string', 'c_promo': 'string'})
print(opfcp.dtypes)


# to be checked: memory_map=True --> uses a memory map to read file, which can improve performance in some environments

# to be checked: partitioning --> (Partitioning or str or list of str, default "hive")
# The partitioning scheme for a partitioned dataset. The default of “hive” assumes directory names with key=value pairs
# like “/year=2009/month=11”. In addition, a scheme like “/2009/11” is also supported, in which case you need to specify
# the field names or a full schema. See the pyarrow.dataset.partitioning() function for more details.

# to be checked: filters --> the actual code implementation and documentation do not match for pyarrow's read_table.


# ********** Saving data into a parquet file

# Simplest way
print('Simple way of writing')

opfcp_parquet = pa.Table.from_pandas(opfcp)                         # converting a pandas dataframe into a pyarrow.Table
pq.write_table(opfcp_parquet, '../data/opfcp_from_pandas.parquet')  # writing the pyarrow.Table data into a parquet file

# opfcp_parquet is the dataframe on which we changed some dataypes before. We can make a test and load the file that
# we have just written. We should have the data types that we changed, for c_ean int32 and for price float64.
opfcp_parquet = pq.read_pandas('../data/opfcp_from_pandas.parquet', columns=['c_ean', 'price'])
opfcp = opfcp_parquet.to_pandas()

print(opfcp.head())
print(opfcp.dtypes)


# More custom way with parameters
print('Customized way of writing')

opfcp_parquet = pa.Table.from_pandas(opfcp,
                                     preserve_index=True,  # to store the index as an additional column
                                     nthreads=1,  # default None; may use up to system CPU count threads and
                                                  # columns are converted in parallel (column / thread)
                                     columns=['c_ean']  # list of columns
                                     )

pq.write_table(opfcp_parquet, '../data/opfcp_ean_only.parquet')
# for more write_table parameters: https://arrow.apache.org/docs/python/generated/pyarrow.parquet.write_table.html

# check whether we really have only c_ean
opfcp = pq.read_pandas('../data/opfcp_ean_only.parquet').to_pandas()
print(opfcp.head())  # yes, we only have the c_ean


# ********** ParquetFile
print('ParquetFile')

pf = pq.ParquetFile('../data/opfcp.parquet')
print(pf.metadata)
print(pf.schema)

# Parquet files may consist of multiple row groups. read_table will read all of the row groups and concatenate them into
# a single table. You can read individual row groups with read_row_group:
print(pf.read_row_group(0))

# We can similarly write a Parquet file with multiple row groups by using ParquetWriter.
# https://arrow.apache.org/docs/python/generated/pyarrow.parquet.ParquetWriter.html


# *******************************************

# To check "Finer-grained Reading and Writing" and "Partitioned Datasets (Multiple Files)" section:
# https://arrow.apache.org/docs/python/parquet.html
