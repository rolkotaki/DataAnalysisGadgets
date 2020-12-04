import dask.dataframe as dd

df = dd.read_parquet('../data/opfcp.parquet')  # blocksize=64000000

ean_count = df['c_ean'].value_counts()
print(ean_count)
ean_count.compute()
print(ean_count.head())

g = df.groupby('c_mag')
# price = g['price']
mean = g['price'].mean()

mean.compute()

print(mean.head())







