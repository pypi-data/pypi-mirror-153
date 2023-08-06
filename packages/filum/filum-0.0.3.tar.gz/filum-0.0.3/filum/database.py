import sqlite3
from sqlite3 import OperationalError, IntegrityError
import pathlib
from filum.helpers import qmarks, current_timestamp

db_name = pathlib.Path(__file__).parent.resolve() / 'filum'


class ItemAlreadyExistsError(Exception):
    pass


class Database(object):
    def __init__(self):
        self._conn = self.connect_to_db(db_name)
        # self._conn.set_trace_callback(print)
        self.sql = dict([
            ('ancestors_sequential', 'SELECT *, ROW_NUMBER() OVER (ORDER BY saved_timestamp DESC) as num FROM ancestors')  # noqa: E501
            ])

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
                'score INTEGER, permalink TEXT UNIQUE, author TEXT, source TEXT,'
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
                    author TEXT, author_id TEXT,
                    score INTEGER, timestamp INTEGER,
                    depth INTEGER);'''
            try:
                self._conn.execute(sql)
            except OperationalError as err:
                print(err)

    def insert_row(self, thread: dict, table_name):
        with self._conn:
            columns = thread.keys()
            values = tuple(thread.values())
            to_insert = f'''({', '.join(columns)}) VALUES ({qmarks(columns)})'''
            sql = f'''INSERT INTO {table_name} ''' + to_insert
            try:
                self._conn.executemany(sql, (values,))
                self._conn.commit()
            except IntegrityError as err:
                # print(err)
                if 'UNIQUE' in str(err):
                    raise ItemAlreadyExistsError

    def update_ancestor(self, thread: dict) -> int:
        with self._conn:
            sql = 'UPDATE ancestors SET saved_timestamp = ?, score = ? WHERE permalink = ?'
            try:
                self._conn.execute(sql, (
                        current_timestamp(),
                        thread['score'],
                        thread['permalink']
                        )
                    )
                id: int = self._conn.execute(
                            ('SELECT ROW_NUMBER() OVER (ORDER BY saved_timestamp DESC) FROM ancestors WHERE permalink = ?'),  # noqa: E501
                            (thread['permalink'], )
                            ) \
                    .fetchone()[0]
            except OperationalError as err:
                print(err)
            return id

    def select_permalink(self, id: int) -> str:
        with self._conn:
            sql = f'WITH a AS ({self.sql["ancestors_sequential"]}) SELECT permalink FROM a WHERE num = ?'
            permalink = self._conn.execute(sql, (id, )).fetchone()[0]
            return permalink

    def select_all_ancestors(self):
        with self._conn:
            sql = self.sql['ancestors_sequential']
            results = self._conn.execute(sql).fetchall()

            return results

    def select_one_ancestor(self, id: int, cond='', **kwargs) -> sqlite3.Row:
        if 'where_param' in kwargs.keys():
            where_param = kwargs['where_param']
            execute_args = (where_param, id)
        else:
            execute_args = (id, )
        with self._conn:
            sql = f'WITH a AS ({self.sql["ancestors_sequential"]} {cond})SELECT * FROM a WHERE num = (?)'
            results = self._conn.execute(sql, execute_args).fetchone()
        return results

    def select_all_descendants(self, id: int, cond='', **kwargs) -> sqlite3.Row:
        if 'where_param' in kwargs.keys():
            where_param = kwargs['where_param']
            execute_args = (where_param, id)
        else:
            execute_args = (id, )
        with self._conn:
            sql = (
                'WITH joined AS ('
                'SELECT d.depth, d.row_id, d.score, d.timestamp, a.id, d.text, d.author, a.num AS key '
                'FROM descendants d '
                f'JOIN ({self.sql["ancestors_sequential"]} a {cond}) a '
                'ON d.ancestor_id = a.id) '
                'SELECT * FROM joined WHERE key = ?'
            )
            results = self._conn.execute(sql, execute_args).fetchall()
            return results

    def get_ancestors_length(self) -> int:
        with self._conn:
            sql = 'SELECT rowid FROM ancestors;'
            results = self._conn.execute(sql).fetchall()
            if results is not None:
                return len(results)
            else:
                return 0

    def delete_ancestor(self, id: int) -> None:
        with self._conn:
            sql_ancestors = '''
                                WITH a AS (
                                    SELECT id, ROW_NUMBER() OVER (ORDER BY saved_timestamp DESC) AS num FROM ancestors
                                )
                                DELETE FROM ancestors WHERE id IN (SELECT id FROM a WHERE num = ?)
                                '''
            self._conn.execute(sql_ancestors, (id,))

    def delete_descendants(self, id: int) -> None:
        with self._conn:
            sql_descendants = '''
                                WITH a AS (
                                    SELECT id, ROW_NUMBER() OVER (ORDER BY saved_timestamp DESC) AS num FROM ancestors
                                )
                                DELETE FROM descendants
                                WHERE ancestor_id IN (SELECT id FROM a WHERE num = ?);
                                '''
            self._conn.execute(sql_descendants, (id,))

    def get_tags(self, id: int) -> str:
        with self._conn:
            sql = (
                f'WITH a AS ({self.sql["ancestors_sequential"]}) '
                'SELECT tags FROM a WHERE num = ?'
                )

            tags = self._conn.execute(sql, (id, )).fetchone()[0]
        return tags

    def update_tags(self, id: int, tags: str):
        '''Update (either add or delete) tags based on user input'''
        with self._conn:
            sql = (
                f'WITH a AS ({self.sql["ancestors_sequential"]}) '
                'UPDATE ancestors SET tags = ? WHERE id IN (SELECT id FROM a WHERE num = ?)'
                )
            self._conn.execute(sql, (tags, id))

    def search(self, column: str, searchstr: str):
        param = f'%{searchstr}%'
        with self._conn:
            sql = (
                'SELECT ROW_NUMBER() OVER (ORDER BY saved_timestamp DESC) as num, '
                f'title, posted_timestamp, saved_timestamp, score, source, tags FROM ancestors WHERE {column} LIKE ?'
            )
            results = self._conn.execute(sql, (param, )).fetchall()
        return results


def main():

    db = Database()
    db.get_ancestors_length()


if __name__ == '__main__':
    main()
