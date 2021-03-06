import sqlite3

# tests

def test_create_db(db):
    assert isinstance(db.conn, sqlite3.Connection)
    assert db.tables == []

def test_define_tables(Author, Book):
    assert Author.name.type == str
    assert Book.author.table == Author

    assert Author.name.sql_type == "TEXT"
    assert Author.age.sql_type == "INTEGER"

def test_create_tables(db, Author, Book):
    db.create(Author)
    db.create(Book)

    assert Author._get_create_sql() == "CREATE TABLE IF NOT EXISTS author (id INTEGER PRIMARY KEY AUTOINCREMENT, age INTEGER, name TEXT);"
    assert Book._get_create_sql() == "CREATE TABLE IF NOT EXISTS book (id INTEGER PRIMARY KEY AUTOINCREMENT, author_id INTEGER, published INTEGER, title TEXT);"

    for table in ("author", "book"):
        assert table in db.tables

def test_create_author_instance(db, Author):
    db.create(Author)

    john = Author(name="John Doe", age=35)
    assert john.name == "John Doe"
    assert john.age == 35
    assert john.id is None

def test_save_author_instances(db, Author):
    db.create(Author)

    john = Author(name="John Doe", age=23)
    db.save(john)

    assert john._get_insert_sql() == (
        "INSERT INTO author (age, name) VALUES (?, ?);",
        [23, "John Doe"]
    )
    assert john.id == 1
    man = Author(name="Man Harsh", age = 28)
    db.save(man)
    assert man.id == 2

    vik = Author(name="Vik Star", age=43)
    db.save(vik)
    assert vik.id == 3

    jack = Author(name="Jack Ma", age=39)
    db.save(jack)
    assert jack.id == 4

def test_query_all_authors(db, Author):
    db.create(Author)
    john = Author(name="John Doe", age=23)
    vik = Author(name="Vik Star", age=43)
    db.save(john)
    db.save(vik)

    authors = db.all(Author)

    assert Author._get_select_all_sql() == (
        "SELECT id, age, name FROM author;",
        ["id", "age", "name"]
    )
    assert len(authors) == 2
    assert type(authors[0]) == Author
    assert {a.age for a in authors} == {23, 43}
    assert {a.name for a in authors} == {"John Doe", "Vik Star"}
