import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import seaborn as sns


# Creating a dataframe
print('Creating dataframes')

df = pd.DataFrame([('Ziggy Stardust', 1), ('Aladdin Sane', 1), ('Pin Ups', 1)], columns=['title', 'toprank'])
# print(df)

df = pd.DataFrame({'title': ['David Bowie', 'The Man Who Sold the World', 'Hunky Dory',
                             'Ziggy Stardust', 'Aladdin Sane', 'Pin Ups', 'Diamond Dogs'],
                   'release': ['1969-11-14', '1970-11-04', '1971-12-17', '1972-06-16',
                               '1973-04-13', '1973-10-19', '1974-05-24']})
# print(df)

df = pd.DataFrame([{'title': 'David Bowie', 'year': 1969},
                   {'title': 'The Man Who Sold the World', 'year': 1970},
                   {'title': 'Hunky Dory', 'year': 1971}])
# print(df)

df2 = pd.DataFrame()
df2['title'] = ['The end of the world', 'Nielsen Split - The Movie']
df2['year'] = [2000, 2020]
# print(df)

df_all = df.append(df2, ignore_index=True)   # appending df2 index to df; the new dataframe will be indexed newly
print(df_all)
df_all = pd.concat([df, df2], axis=0)        # df and df2 are concatenated; as ignore_index is False by default,
print(df_all)                                # the existing index is kept

# from numpy array
np_array = np.array([[1.1, 11.1],
                     [2.2, 22.2],
                     [3.3, 33.3],
                     [4.4, 44.4],
                     [np.nan, 55]])
df_numpy = pd.DataFrame(np_array, columns=['num1', 'num2'])
df_numpy.dropna(inplace=True)  # dropping records with np.nan values; with inplace=True it is applied on the df itself
print(df_numpy)

# Creating a new row (Series object)
new_movie = pd.Series(['Star Wars - The Last Jedi', 2017], index=['title', 'year'])
df_all = df_all.append(new_movie, ignore_index=True)
print(df_all)


# Reading data from file into pandas dataframe

odf = pd.read_csv('../data/olympics.csv', skiprows=5,
                   names=['city', 'edition', 'sport', 'discipline', 'athlete', 'noc', 'gender',
                          'event', 'Event_Gender', 'medal'])  # other parameters also: sep; skip_blank_lines

print(odf.head())      # first 5 rows by default, but we can pass another number as a parameter
odf.tail()             # last 5 rows by default
print(len(odf))        # number of rows
print(odf.dtypes)      # column data types
print(odf.describe())  # gives general information about the dataframe, such as: count, min, max values (of num columns)


# Basic operations on a dataframe
print('basic operations')

odf.city.unique()        # returns a list of unique city values
odf['city'].unique()     # same as before
odf.city.nunique()       # number of unique values
odf.city.value_counts()  # returns the count value for each city
odf.city.value_counts(dropna=False)  # taking into account NaN values as well

print(odf.edition.min())  # prints out the min year (edition)
odf.edition.max()         # returns the max year (edition)
odf.edition.mean()        # doesn't make sense here, just an example
# there are also sum, count, all the others ...

odf.duplicated(subset=['city', 'edition', 'sport', 'discipline'])  # shows if record is duplicated or not; boolean list

odf.drop_duplicates()     # dropping duplicated (if all columns match)
# dropping  duplicated if the following four columns match and keeping last record
odf.drop_duplicates(subset=['city', 'edition', 'sport', 'discipline'], keep='last')

odf.rename(columns={'Event_Gender': 'event_gender'}, inplace=True)                     # renaming a column(s)
odf['event_gender'].replace(['M', 'W'], ['Men', 'Women'], inplace=True)  # replacing value(s) in a column

# function on all items
def to_upper(s):
    return s.upper()


odf.sport.apply(to_upper)             # applying the to_upper() function to all elements
odf.sport.apply(lambda s: s.upper())  # the same as before, but with a lambda function. this is a nicer solution

# more examples to apply functions on all items later


# Sorting the datadrame

odf.city.sort_values()                 # returns the city column as sorted
odf.sort_values('city', inplace=True)  # sorts the dataframe by city; inplace=True means that the sorting is applied
odf.sort_values(by=['edition', 'city'], ascending=False, inplace=True)  # sorting by multiple columns


# Filtering data
print('Filtering data')

odf_athens = odf[odf['city'].isnull()]     # filtering for NaN (NULL) values
odf_athens = odf[odf['city'].notnull()]    # excluding NaN values
odf_athens = odf[odf['city'] == 'Athens']
odf_athens = odf[odf.city.str.contains('Athens')]  # string operations available on Series (column) objects with strings
odf_athens = odf[odf.city == 'Athens']

odf_athens_2004 = odf[(odf['city'] == 'Athens') & (odf['edition'] == 2004)]
odf_athens_2004 = odf.query('city=="Athens" and edition==2004')

odf.drop([0, 1], axis=0)         # deleting first two rows; with inplace=True it is applied on the dataframe


# Indexing
print('Indexing')

print(odf.index)  # by default we have an integer index

odf_by_edition = odf.set_index(odf['edition'])            # here an index is created from the values of edition column
odf_by_edition = odf.set_index('edition')                 # setting index to a single column; column itself is the index
odf_by_city_edition = odf.set_index(['city', 'edition'])  # setting index to multiple columns
odf_by_city_edition.sort_index(inplace=True)              # sorting the index

odf_by_edition.reset_index(inplace=True)                 # returning to the default integer index, resetting it
odf_by_edition.set_index('edition', inplace=True)        # setting the index in place, meaning it is applied on the df

print(odf_by_city_edition)


# Getting rows by indexes : loc and iloc  -  label-based indexing for selection by label (loc)
print('loc and iloc')

odf_by_edition.loc[2004]                # selecting rows by the index; using loc
odf_by_edition.loc[2008, 'sport']       # selecting rows by index (edition=2008), but ONLY the sport column

odf_by_edition.sort_index(ascending=True, inplace=True)  # sorting the index in ascending order, applying it on the df
odf_by_edition.loc[2004:2008]  # selecting rows by the index, searching by multiple values

odf_by_city_edition.loc['Athens']        # using loc with only the first index column
odf_by_city_edition.loc['Athens', 1896]  # using loc with multiple index columns

odf_by_city_edition.loc[(['Athens', 'Berlin'], slice(1896, 2004)), :]  # using slicer for index searching
odf_by_city_edition.loc[(['Athens', 'Berlin'], slice(None)), :]        # slice(None) = ALL; ":" means all columns
print(odf_by_city_edition.loc[(['Athens', 'Berlin'], slice(1896, 2004)), :])

odf_by_city_edition.index.get_level_values(0)  # returns the values of the first index column

odf_by_city_edition.iloc[0:10]  # with iloc we can search by the defaults integer index, even if we have a custom index
odf_by_city_edition.iloc[0]

# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.loc.html


# Adding and dropping columns
print('adding new columns')

odf['sport_discipline'] = odf['sport'] + ' ' + odf['discipline']  # adding new column for sport and discipline
calc_century = np.vectorize(lambda year: math.floor(year / 100)+1)  # a vectorized function to be used on each element
odf['century'] = calc_century(odf['edition'])                     # adding new column for the century
odf['century'] = [math.floor(year / 100)+1 for year in odf['edition']]  # the same result as above
odf['double_year'] = odf['edition'] * 2                           # it doesn't make sense, just an example
odf['double_year'] = odf['edition'] + odf['edition']              # same result as before
odf['log_year'] = np.log10(odf['edition'])                        # just an example on how to use numpy's math functions
print(odf.head())

odf.drop('log_year', axis=1, inplace=True)  # dropping log_year column; for multiple columns list parameter as always
odf.drop(odf.columns[8], axis=1)            # column can be dropped by its index


# Merging dataframes
print('merging dataframes')

gapminder = pd.read_csv('../data/gapminder.csv')  # loading another dataframe for more numerical columns
hungary = gapminder[gapminder.country == 'Hungary']
spain = gapminder[gapminder.country == 'Spain']

hun_spain = pd.merge(hungary, spain, on='year', how='inner')             # inner join is the default; 15 columns
# print(hun_spain)
hun_spain = pd.merge(hungary, spain, on=['region', 'year'], how='left')  # left join; 14 columns (2 will be common)
# print(hun_spain)

spain = spain.rename(columns={'year': 'ano'})
hun_spain = pd.merge(hungary, spain, left_on='year', right_on='ano')  # if the column names are different; 16 columns
print(hun_spain)
# print(len(hun_spain))


# Grouping
print('grouping')

gapminder.groupby('year').babies_per_woman.mean()  # average of babies per woman after grouping data by year
gapminder.groupby('year').size()                   # count for groups
gapminder.groupby(['region', 'year']).babies_per_woman.mean()       # group by multiple columns
gapminder.groupby(['region', 'year'])['babies_per_woman'].mean()  # same as before; if column name has space, this works
# the aggregation functions run on each columns in the below example
gapminder_grouped = gapminder.groupby(['region', 'year']).agg(['min', 'max', 'count'])  # multiple aggregation functions
print(gapminder_grouped.head())
# the aggregation functions run only on the babies_per_woman column in the below example
gapminder_grouped = gapminder.groupby(['region', 'year']).babies_per_woman.agg(['min', 'max', 'count'])
print(gapminder_grouped.head())
# the below example is almost the same as the previous one, however now we have "babies_per_woman" as column title
# and this way we can define multiple options
gapminder_grouped = gapminder.groupby(['region', 'year']).agg({'babies_per_woman': ['min', 'max', 'count']})
print(gapminder_grouped.head())

# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.core.groupby.DataFrameGroupBy.filter.html

# we can loop through the groups in a grouped dataframe
gapminder_grouped = gapminder.groupby(['region', 'year'])
for name, group in gapminder_grouped:
    # print(name)
    # print(group.babies_per_woman.sum())
    pass

# it is also possible to group rows by times (weekly, monthly, etc). We can also have a time-indexed dataframe.


# Pivot tables
print('pivot tables')

# year: row identifier; region: column identifier; values: babies_per_woman
pivot_df = gapminder.pivot_table('babies_per_woman', 'year', 'region')  # worth checking all possible parameters
print(pivot_df.head())


# unstack and stack
print('stack and unstack')

print('unstacked')
# Athletes winning medals in Beijing Olympics 100m or 200m track event
mw = odf[(odf.edition == 2008) & ((odf.event == '100m') | (odf.event == '200m'))]  # filtering for year and event
g = mw.groupby(['noc', 'gender', 'discipline', 'event']).size()                    # grouping by + getting group counts
unstacked_df = g.unstack(['discipline', 'event'])                                  # turning rows to columns
print(unstacked_df.head())
print('stacked')
stacked_df = unstacked_df.stack('event')                                           # turning columns to rows
print(stacked_df)
print('unstacked')
stacked_df = unstacked_df.unstack('gender')
print(unstacked_df)


# Plotting

# Some diagrams/charts about the number of Sport categories in the 2004 Olympic Games
odf_athens_2004 = odf[odf.edition == 2004]

odf_athens_2004.sport.value_counts().plot(kind='line')                                  # by default a line plot
plt.show()
odf_athens_2004.sport.value_counts().plot(kind='bar', color='blue', figsize=(8, 6))
plt.show()
odf_athens_2004.sport.value_counts().plot(kind='barh')                                  # horizontal bars
plt.show()
odf_athens_2004.sport.value_counts().plot(kind='pie', colormap='Pastel1')               # colormap can be custom also
plt.savefig('../charts/pie_chart.png')
plt.show()

# We can also build up a plot from the beginning:
plt.figure(figsize=(8, 8))
plt.title('Number of sports')
plt.plot(odf_athens_2004.sport.unique(), odf_athens_2004.sport.value_counts())
plt.show()

# more advanced charts: seaborn - this is (also) to be investigated further
sns.countplot(data=odf, x='medal', hue='gender')
plt.savefig('../charts/sns_chart.pdf')
plt.show()

# sns.countplot(data=odf_athens_2004, x='medal', hue='gender', palette='seismic', order=['gold', 'silver', 'bronze'])
