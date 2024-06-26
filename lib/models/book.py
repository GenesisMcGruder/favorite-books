import re
from models.__init__ import CURSOR, CONN
from models.genre import Genre

class Book:
    all = {}
    def __init__(self, name, author, page_count, genre_id, id=None):
        self.id = id
        self.name = name
        self.author = author
        self.page_count = page_count
        self.genre_id = genre_id

    # def __repr__(self):
    #     return (
    #         f'Book: {self.name}, {self.author}, {self.page_count}' +
    #         f'Genre: {Genre.genre}'
    #         )
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,name):
        pattern = r'^[a-zA-Z0-9\s,]+$'
        if re.match(pattern, name):
            self._name = name
        else:
            raise ValueError("Name must be an alphanumeric character")

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, author):
        if isinstance(author, str):
            self._author = author
        else:
            raise ValueError("Author must be a string")

    
    @property
    def page_count(self):
        return self._page_count

    @page_count.setter
    def page_count(self, page_count):
        if isinstance(page_count, int):
            self._page_count = page_count
        else:
            raise ValueError("Page count must be a number")


    @property
    def genre_id(self):
        return self._genre_id

    @genre_id.setter
    def genre_id(self, genre_id):
        if type(genre_id) is int and Genre.find_by_id(genre_id):
            self._genre_id = genre_id
        else:
            raise ValueError("Must be a genre reference")


    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                name TEXT,
                author VARCHAR(100),
                page_count INTEGER,
                genre_id INTEGER
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS books;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = """
           INSERT INTO books (name, author, page_count, genre_id)
           VALUES (?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.name,self.author,self.page_count, self.genre_id,))
        CONN.commit()

        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, author, page_count, genre_id):
        book = cls(name,author, page_count, genre_id )
        book.save()
        return book

    # def update(self):
    #     sql = """
    #         UPDATE books
    #         SET name = ?, author = ?, page_count = ?, genre_id = ?
    #         WHERE id = ?
    #     """
    #     CURSOR.execute(sql, (self.name, self.author,self.page_count, self.genre_id, self.id))
    #     CONN.commit()

    @classmethod
    def delete(cls, book):
        sql = """
            DELETE FROM books
            WHERE id = ?
        """
        CURSOR.execute(sql, (book.id,))
        CONN.commit()

        del cls.all[book.id]

    @classmethod
    def instance_by_db(cls, row):
        book = cls.all.get(row[0])
        if book:
            book.name = row[1]
            book.author = row[2]
            book.page_count = row[3]
            book.genre_id = row[4]
        else:
            book = cls(row[1],row[2], row[3], row[4])
            book.id = row[0]
            cls.all[book.id] = book
        return book

    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM books
        """
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_by_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT *
            FROM books
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()
        return cls.instance_by_db(row) if row else None

    @classmethod
    def find_by_name(cls,name):
        sql = """
            SELECT *
            FROM books
            WHERE name = ?
        """
        row = CURSOR.execute(sql, (name,)).fetchone()
        return cls.instance_by_db(row) if row else None

    @classmethod
    def find_by_author(cls, author):
        sql= """
            SELECT *
            FROM books
            WHERE author = ?
        """
        row = CURSOR.execute(sql, (author,)).fetchone()
        return cls.instance_by_db(row) if row else None
