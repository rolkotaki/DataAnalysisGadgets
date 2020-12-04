import datetime
import multiprocessing as mp
import numpy as np
import pandas as pd


# print(datetime.datetime.now().strftime("%H:%M:%S"), ' begin')

np_array = np.arange(1, 1000000, 1)
df = pd.DataFrame(np_array, columns=['num'])
chunksize = 200000
# print(datetime.datetime.now().strftime("%H:%M:%S"), ' df created')

def calc_sinus(i):
    # df[i:i + chunksize]['sin_with'] = np.sin(df[i:i + chunksize]['num'])
    for row in range(i, i+chunksize):
        n = np.sin(df[row].num ** 4)


if __name__ == '__main__':
    # df['sin_without'] = np.sin(df.num)
    # print(df.head())
    print(datetime.datetime.now().strftime("%H:%M:%S"), ' begin')
    for row in range(0, len(df)):
        n = np.sin(df[row].num**4)

    print(datetime.datetime.now().strftime("%H:%M:%S"), ' sin calculated WITHOUT multiprocessing')

    pool = mp.Pool(processes=4)
    results = pool.map(calc_sinus, range(0, len(df), chunksize))
    pool.close()
    # print(df.head())
    print(datetime.datetime.now().strftime("%H:%M:%S"), ' sin calculated WITH multiprocessing')

