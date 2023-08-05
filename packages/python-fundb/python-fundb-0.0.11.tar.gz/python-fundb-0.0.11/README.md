# FunDB

**FunDB** is Hybrid Row-and-Document Oriented datastore leveraging SQL/RDBMS database: SQLite, MySQL, MariaDB, Postgresql 

FunDB is both RDMBS + Document Oriented together.

It supports, regular SQL query along with Document Oriented and Key Value store.

Engine:
- JSON
- SQLite
- Mariadb
- PostgreSQL
- MySQL



### Install

```python 
pip install python-fundb
```

### Usage


```python
from fundb import fundb

# Open the db
# or in memory > fun = fundb()
fun = fundb("./my.db")

# Select a collection. 
# Collection will be created automatically
# or explicitely > test = fun.select('test')
test = fun.test

# Get total entries
print(test.size)

# Insert an entry. It returns fundb#Document
entry = test.insert({
  "name": "Fun",
  "type": "DB",
  "version": "1.0.0"
})

# Retrieve document by _id
_id = "9c5e5fbd05544700995c5fa3ca3ef214"
entry = test.get(_id)

# Access properties
entry.name # -> fun 
entry.type # -> DB
entry.version # -> 1.0.0

# Update a field
entry.update(version="1.0.1")
# ...or 
entry.update({"version": "1.0.1"})
#
entry.version # -> 1.0.1

# Delete entry
entry.delete()

# Search
results = test.find({"version:$gt": "1.0.0"})
for entry in results:
  print(entry.name)


```

## ~ API ~

## Database

### fundb

### #select

To select a collection in the database

```python
fun = fundb()

users = fun.select("users")

## or 

users = fun.users
```


### #collections

List all the collections in the database 

```python
fun = fundb()

users = fun.select("users")

## or 

users = fun.users
```

##D


