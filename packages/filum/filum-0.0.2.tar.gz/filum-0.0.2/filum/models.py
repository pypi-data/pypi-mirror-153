import sqlite3
from sqlite3 import OperationalError, IntegrityError
import pathlib

db_name = pathlib.Path(__file__).parent.resolve() / 'filum'


class ItemAlreadyExistsError(Exception):
    pass


class FilumModel(object):
    def __init__(self):
        self._conn = self.connect_to_db(db_name)
        # self._conn.set_trace_callback(print)
        with self._conn:
            self.create_table_ancestors()
            self.create_table_descendants()

    def connect_to_db(self, db=None):
        if db is None:
            my_db = ':memory:'
            print('New connection to in-memory SQLite db')
        else:
            my_db = f'{db}.db'
        conn = sqlite3.connect(my_db)
        # Return Row object from queries to allow accessing columns by name
        conn.row_factory = sqlite3.Row
        return conn

    def create_table_ancestors(self):
        with self._conn:
            sql = (
                'CREATE TABLE IF NOT EXISTS ancestors'
                '(row_id INTEGER PRIMARY KEY AUTOINCREMENT,'
                'id TEXT, title TEXT, body TEXT, posted_timestamp INTEGER, saved_timestamp INTEGER, '
                'score INTEGER, permalink TEXT UNIQUE, num_comments INTEGER, author TEXT, source TEXT,'
                'tags TEXT);'
            )

            try:
                self._conn.execute(sql)
            except OperationalError as err:
                print(err)

    def create_table_descendants(self):
        with self._conn:
            sql = '''CREATE TABLE IF NOT EXISTS descendants
                    (row_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ancestor_id INTEGER REFERENCES ancestors(row_id),
                    id TEXT,
                    parent_id TEXT,
                    text TEXT, permalink TEXT,
                    author TEXT, author_id TEXT, is_submitter INTEGER,
                    upvotes INTEGER, downvotes INTEGER, score INTEGER, timestamp INTEGER,
                    depth INTEGER, path TEXT,
                    FOREIGN KEY (parent_id) REFERENCES descendants(id));'''
            try:
                self._conn.execute(sql)
            except OperationalError as err:
                print(err)

    def insert_row(self, thread: dict, table_name):
        with self._conn:
            columns = thread.keys()
            values = tuple(thread.values())
            to_insert = f'''({', '.join(columns)}) VALUES ({', '.join(['?']*len(columns))})'''
            sql = f'''INSERT INTO {table_name} ''' + to_insert
            try:
                self._conn.executemany(sql, (values,))
                self._conn.commit()
            except IntegrityError as err:
                print(err)
                if 'UNIQUE' in str(err):
                    raise ItemAlreadyExistsError

    def select_all_ancestors(self):
        with self._conn:
            sql = '''
                    SELECT (SELECT COUNT(*) FROM ancestors b WHERE a.row_id >= b.row_id) AS num,
                    title, posted_timestamp, saved_timestamp, score, source, tags
                    FROM ancestors a;'''

            sql = '''
                    SELECT ROW_NUMBER() OVER (ORDER BY saved_timestamp) as num,
                    title, posted_timestamp, saved_timestamp, score, source, tags
                    FROM ancestors a
            '''
            results = self._conn.execute(sql).fetchall()

            return results

    def select_one_ancestor(self, columns: list, id: int) -> sqlite3.Row:
        with self._conn:
            columns = ', '.join(columns)
            sql = (
                'WITH a AS ('
                'SELECT *, (SELECT COUNT(*) FROM ancestors b WHERE ancestors.row_id >= b.row_id) AS num FROM ancestors)'
                f'SELECT {columns} FROM a WHERE num = (?)'
            )
            sql = f'''
                    WITH a AS (
                        SELECT *, ROW_NUMBER() OVER (ORDER BY saved_timestamp) as num FROM ancestors
                        )
                    SELECT {columns} FROM a WHERE num = (?)

            '''
            results = self._conn.execute(sql, (id, )).fetchone()
            return results

    def select_all_descendants(self, id: int) -> sqlite3.Row:
        with self._conn:
            sql = '''
                WITH joined AS (
                    SELECT d.depth, d.row_id, d.score, d.timestamp, a.id, d.text, d.author, a.num AS key
                    FROM descendants d
                    JOIN (SELECT *, ROW_NUMBER() OVER (ORDER BY saved_timestamp) AS num FROM ancestors a) a
                    ON d.ancestor_id = a.id
                    )
                SELECT * FROM joined WHERE key = ?
            '''
            results = self._conn.execute(sql, (id,)).fetchall()
            return results

    def get_ancestors_length(self) -> int:
        with self._conn:
            sql = 'SELECT rowid FROM ancestors;'
            results = self._conn.execute(sql).fetchall()
            if results is not None:
                return len(results)
            else:
                return 0

    def delete(self, id) -> sqlite3.Row:
        # TODO: Rewrite this so that a col is added to ancestors which contains
        # the row_number() values to avoid creating a new table every time the
        # commands "thread" and "all" are run
        with self._conn:
            sql_descendants = '''
                                WITH a AS (
                                    SELECT id, ROW_NUMBER() OVER (ORDER BY saved_timestamp) AS num FROM ancestors
                                )
                                DELETE FROM descendants
                                WHERE ancestor_id IN (SELECT id FROM a WHERE num = ?);
                                '''
            sql_ancestors = '''
                                WITH a AS (
                                    SELECT id, ROW_NUMBER() OVER (ORDER BY saved_timestamp) AS num FROM ancestors
                                )
                                DELETE FROM ancestors WHERE id IN (SELECT id FROM a WHERE num = ?)
                                '''
            self._conn.execute(sql_descendants, (id,))
            self._conn.execute(sql_ancestors, (id,))


def main():

    db = FilumModel()
    db.get_ancestors_length()


if __name__ == '__main__':
    main()
