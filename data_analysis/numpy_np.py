import numpy as np
from scipy import sparse


# https://numpy.org/devdocs/reference/index.html
# There are so many numpy functions that it is impossible to cover everything.
# The documentation above is very good, good explanations for parameters and they show examples also.


# Creating a numpy array from list(s)
print('creating numpy arrays')

vector_column = np.array([[1], [2], [3]])
vector_row = np.array([1, 2, 3], np.int32)  # by default it is int64, we can specify the data type
vector_row[:]     # all elements of the vector; [1 2 3]
vector_row[1:]    # all elements after the first; [2 3]
vector_row[:1]    # all elements up to and including the first; [1]
vector_row[-1]    # last element; 3

print(np.array([vector_row]).T)  # transposing row vector to column vector
print(vector_column.flatten())   # transforming the matrix into a one-dimensional array)

from_list = np.array([[1, 2, 3],
                      [4, 5, 6],
                      [7, 8, 9]])  # we can call this a matrix also (2 dimensional array)
print(from_list)
print(from_list[1][2])  # 6
from_list[1, 2] = 66
print(from_list[1, 2])  # 66

from_list[:2, :]   # the first two rows and all columns
from_list[:, 1:2]  # all rows and the second column (indexing starts from 0)


# Mathematical operations on a numpy array
np.min(from_list)          # returns only one value, the sum
np.max(from_list, axis=0)  # maximum element in each column
np.max(from_list, axis=1)  # maximum element in each row
np.max(from_list)
np.sum(from_list)
np.mean(from_list)
np.sin(from_list)  # returns a new array with the the sinus values of all elements
np.cos(from_list)
np.arctan(from_list)
np.abs(from_list)
np.std(from_list)  # standard deviation; important for machine learning for example
# ...
np.nansum(from_list)
np.nanmin(from_list)  # if the numpy array contains NaN values
# ...

# operations on each element
array_100 = from_list + 100  # adding 100 to each element
vectorized_add_100 = np.vectorize(lambda i: i + 100)  # vectorizing the lambda function that adds 100 to an element
array_100 = vectorized_add_100(from_list)
print(array_100)

# adding items to numpy array
print('adding elements to numpy array')

from_list = np.array([[1, 2, 3],
                      [4, 5, 6],
                      [7, 8, 9]])
# after adding a new item, the array will become a vector, meaning one dimension, we will have to reshape it
# if we add a new row, then we have to increase the row number with one, leaving the column number untouched
new_shape = (from_list.shape[0] + 1, from_list.shape[1])
from_list = np.append(from_list, [[0, 1, 2]])  # appending the new item
print(from_list)
from_list = from_list.reshape(new_shape)  # reshaping
print(from_list)

# If we use the axis parameter, we don't have to worry about reshaping
from_list = np.append(from_list, [[9, 9, 9]], axis=0)  # axis=0 meaning row
print(from_list)
from_list = np.append(from_list, [[8], [8], [8], [8], [8]], axis=1)  # axis=1 meaning column
print(from_list)

from_list = np.insert(from_list, 1, [[-1, -1, -1, -1]], axis=0)  # inserint new row at index 1 (second row)
print(from_list)
from_list = np.insert(from_list, 1, [[-1, -1, -1, -1, -1, -1]], axis=1)  # inserting new column at index 1 (second col)
print(from_list)

from_list = np.delete(from_list, 1, axis=0)  # deleting the row at index 1 (second row)
from_list = np.delete(from_list, 1, axis=1)  # deleting the column at index 1 (second col)
print(from_list)


# joining arrays
print('joining arrays')
a = [[0, 1], [2, 3]]
b = [[4, 5]]
joined = np.concatenate((a, b), axis=0)
print(joined)
joined = np.concatenate((joined, joined), axis=1)
print(joined)

# splitting arrays
print('splitting arrays')
split = np.split(joined, 3, axis=0)  # second parameter says into how many arrays it should be split
print(split)
split = np.split(joined, 4, axis=1)
print(split)

# numpy's nan value means NULL, nothing ...
features = np.array([[1.1, 11.1],
                     [2.2, 22.2],
                     [np.nan, 55]])

# It is worth checking out the matrix operations with numpy. Matrix operations are highly supported.


# Creating dummy numpy arrays
print('dummy arrays with numpy')

zeros_1d = np.zeros(8, 'd')             # 'd' --> data type; we could also use np.float64
ones_2d = np.ones((8, 8), np.float64)   # an 8 row 8 column 2 dimensional array filled with ones
print(zeros_1d)
print(ones_2d)

rand_2d = np.random.random(size=(8, 8))  # an 8 row 8 column 2 dimensional array filled with random numbers (0-1)
print(rand_2d)
rand = np.random.randint(0, 11, 3)       # three random integers between 1 and 10

linear = np.linspace(0, 1, 15)  # an array having 15 items, equally distributed between 0 and 1, including both
print(linear)


# Sparse matrix
print('sparse matrix')

matrix_zero = np.mat([[1, 0, 0], [0, 0, 0], [0, 6, 0]])
matrix_sparse = sparse.csr_matrix(matrix_zero)  # creating a compressed sparse row matrix (csr)

# Sparse matrices only store nonzero elements and assume all other values will be zero, leading to
# significant computational savings
print(matrix_sparse)
# (0, 0)    1
# (2, 1)    6
# In compressed sparse row (CSR) matrices, (0, 0) and (2, 1) represent the indices of the non-zero values.


# Creating a numpy array from file
print('creating numpy array from file')

monalisa = np.loadtxt('../data/monalisa.txt')  # delimiter, skiprows, usecols (which columns to load)
# np.savetxt('monalisa_2.txt', monalisa)
print(monalisa.ndim)   # returns the number of rows and columns
print(monalisa.shape)  # dimensions
print(monalisa.size)   # number of items
print(monalisa.dtype)  # datatype


# We can also load from and save into npy files
print('numpy array from npy file')
monalisa_npy = np.load('../data/monalisa.npy')  # rgb colours of the picture
# np.save('monalisa_2.npy', monalisa_npy)
print(monalisa_npy[600, 400])
print(monalisa_npy[600][400])     # same result
print(monalisa_npy[600, 400, 0])  # row, column, index in the list (RGB has 3 values)

monacopy = monalisa_npy.copy()  # copying a numpy array


print('numpy array from txt file (fixed-width columns)')
# Loading a fixed-width text file: we prescribe the widths of every field; other cases the delimiter can be a character.
# The names of the resulting array columns; their data types. 'Uxx' stands for unicode string of length xx;
# 'd' for double precision floating point
stations = np.genfromtxt('../data/stations.txt',
                         delimiter=[11, 9, 10, 7, 3, 31, 4, 4, 6],
                         names=['id', 'latitude', 'longitude', 'elevation', 'state', 'name', 'gsn', 'hcn', 'wmo'],
                         dtype=['U11', 'd', 'd', 'd', 'U3', 'U31', 'U4', 'U4', 'U6'],
                         autostrip=True)  # to remove spaces

# Filtering data in a numpy array
stations_ca = stations[stations['state'] == 'CA']  # creating a new array with only Californian data
pasadena = stations[stations['name'] == 'PASADENA']
pasadena = stations[(stations['state'] == 'CA') & (stations['name'] == 'PASADENA')]  # & and | operators work
pasadena = stations[np.char.find(stations['name'], 'PASADENA') == 0]  # another way, similar to PLSQL's instr()

pasadena_min = np.nanmin(pasadena['elevation'])  # returns the min value of the elevation column; works with NaN values
print(pasadena_min)

np_array = np.array([[1.1, 11.1],
                     [2.2, 22.2],
                     [3.3, 33.3],
                     [4.4, 44.4],
                     [np.nan, 55]])
without_nan = np_array[~np.isnan(np_array).any(axis=1)]  # filtering out records with NaN values


# For us this is not an issue if an array has NaN / NULL values, but just to point out as something interesting:
# fill NaNs in any array by linear interpolation
def fillnans(array):
    good = ~np.isnan(array)
    x = np.arange(len(array))
    return np.interp(x, x[good], array[good])
