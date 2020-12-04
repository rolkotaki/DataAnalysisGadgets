import collections


# Lists

nrps_list = ["Julien", "Rafael"]
len(nrps_list)                                       # length of the list
nrps_list.append('Javier')                           # add a new item after the last one
nrps_list.extend(['Miguel', 'Gregory'])              # adds multiple items
nrps_list.insert(2, 'Sergio')                        # inserts a new item with index=2

nrps_list.index('Sergio')                            # returns the index of the item
nrps_list[0]                                         # referencing the first item of the list
nrps_list[1:3]                                       # items starting from the second till the third
nrps_list[2]                                         # all items starting from the third
nrps_list.count('Rafael')                            # counts the item in the list
nrps_list[0] = 'Julien - Boss'

nrps_list.remove('Gregory')                          # removes the item
last_item = nrps_list.pop()                          # removes and returns the last item

new_list = nrps_list + ['Miguel', 'Gregory', 'Roland', 'Gleb']  # merging two lists

new_list.sort()                                      # ordering the list (applied on the given list in place)
new_list.sort(reverse=True)                          # ordering the list in reverse order
new_list.reverse()                                   # ordering the list in reverse order
reverse_list = sorted(new_list, reverse=True)        # ordering in reverse order

if new_list.__contains__('Gregory'):
    print('Gregory is a member of the team.')

print(new_list)

mixed_list = [1, [2, 3], 'alpha']                    # a list can contain different types of values
mixed_list.clear()


# Tuples - read-only lists

numbers = ('one', 'two', 'three', 'four')
print(len(numbers))
print(numbers.count('one'))
print(numbers.index('one'))
# numbers[0] = 1  # TypeError: 'tuple' object does not support item assignment


# Dictionaries

capitals = {'United States': 'Washington, DC', 'France': 'Paris', 'Italy': 'Rome'}
morecapitals = {'Germany': 'Berlin', 'United Kingdom': 'London'}
capitals['Spain'] = 'Madrid'       # adding new key-value pair
capitals.update(morecapitals)      # merging the two dictionaries
del capitals['United Kingdom']     # deleting a key-value pair
capitals.keys()                    # returns the countries
capitals.values()                  # returns the capitals
capitals.items()                   # returns both the keys and values
print(capitals.get('Spain'))       # returns the value for the given key


# Sets - no duplicates

continents = {'America', 'Europe', 'Asia', 'Oceania', 'Africa', 'Africa'}  # only one item as 'Africa'
continents.add('Antarctica')
continents.remove('Antarctica')
continents.add('America')  # it will not add it again as the set already contains 'America'
print(continents)
continents.pop()


# Named Tuples

persontype = collections.namedtuple('person', ['firstname', 'lastname', "birthday"])
roland = persontype("Roland", "Takacs", "February 31")
roland = persontype(lastname="Takacs", firstname="Roland", birthday="February 31")
print(roland[0], roland[1], roland[2])
print(roland.firstname, roland.lastname, roland.birthday)

people = [("Michele", "Vallisneri", "July 15"),
          ("Albert", "Einstein", "March 14"),
          ("John", "Lennon", "October 9"),
          ("Jocelyn", "Bell Burnell", "July 15")]

persontype(*people[0])
# A tuple item in the people list could have whatever number of values. In Python, instead of having to pass the
# values one by one, we can use * to pass all values. This way we don't have to know the exact number.
namedpeople = [persontype(*person) for person in people]  # adding


# DefaultDict

def mydefault():
    return "Life is good"


questions = collections.defaultdict(mydefault)
print(questions['The meaning of life'])  # if the key doesn't exist in the dictionary, the default value is returned

birthdays = collections.defaultdict(list)
for person in namedpeople:
    birthdays[person.birthday].append(person.firstname)
# we don't have to check if there is already a name for that birthday. if yes, the name will have multiple birthdays
print(birthdays)

# or we can use SET with the ADD method
birthdays = collections.defaultdict(set)
for person in namedpeople:
    birthdays[person.birthday].add(person.firstname)
# we don't have to check if there is already a name for that birthday. if yes, the name will have multiple birthdays
print(birthdays)


# Comprehensions

squares = [i**2 for i in range(1, 11)]
squares_by_four = [i**2 for i in range(1, 11) if i**2 % 4 == 0]
print(squares_by_four)

capitals_by_country = {'United States': 'Washington, DC', 'France': 'Paris', 'Italy': 'Rome'}
countries_by_capital = {capital: country for country, capital in capitals_by_country.items()}

print(sum(i**2 for i in range(1, 11)))

counting = [j for i in range(1, 11) for j in range(1, i+1)]
print(counting)
