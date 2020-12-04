import pyarrow.parquet as pq


parq_table = pq.read_table('../data/opfcp.parquet')  # loading the parquet file into a pyarrow.Table object

# Convert the Table to a dictionary (columnar dictionary: one key (column) having a list of values (row data))
table_dict = dict(parq_table.to_pydict())
# converting it to a list of dictionaries (I think it is incorrect, it is a list of tuples actually)
# a tuple, whose first element is the column name, the second element is a list of all the row data values
items = table_dict.items()
# getting the keys (column names)
keys = [item[0] for item in items]  # as mentioned before, the first element of the tuple is the column name
# getting the values (row data)
values = [item[1] for item in items]  # the second item in the tuple is the list of all row data values
# zipping the values together
pivoted_values = list(zip(*values))
# From Python documentation about zip:
# Returns a zip object whose .__next__() method returns a tuple where the i-th element comes from the i-th iterable
# argument.  The .__next__() # method continues until the shortest iterable in the argument sequence is exhausted
# and then it raises StopIteration.

# zipping the column with the corresponding value, then converting it to a dictionary and appending it to an array
table_dictionary_array = []
for record in pivoted_values:
    table_dictionary_array.append(dict(zip(keys, record)))

# At the end, we will have a list of dictionaries with the normal row data (not the columnar data)
print(table_dictionary_array[0:5])  # checking the first 5 rows
