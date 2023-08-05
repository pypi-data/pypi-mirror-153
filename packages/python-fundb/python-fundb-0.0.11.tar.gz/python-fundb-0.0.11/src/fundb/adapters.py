
import sqlite3
import pymysql
import sqlparams
from typing import Any, List
from urllib.parse import urlparse
from dbutils import steady_db


def convert_qmark_query_to_adapter_style(query, params, to_format="format"):
    """
    By default fundb support qmark query style -> '?'
    But some adapter, ie pymysql, supports 'format' style -> '%s'
    This utility will help reformat the qmark to the respective format

    Args:
        query:str - The query with the qmark
        params:tuple - 
        to_format:str

    Returns:
        tuple(query:str, params:dict|tuple)
    """
    from_format = "qmark"
    _sqlparams = sqlparams.SQLParams(from_format, to_format)
    return _sqlparams.format(query, params)


class Adapter(object):
    """
    Base Adapter class
    """


    # Holds the db connection
    db = None

    # The engine: sqlite, mysql for (mysql|mariadb), postgresql 
    engine = None

    def execute(self, query: str, params: Any = None) -> Any:
        """
        Executes a query
        Args:
            query: str
            params: tuple()
        
        Returns:
            Cursor
        """
        raise NotImplementedError()

    def create_collection(self, table):
        """
        Create a collection

        Args:
            table:str - the collection name

        Returns:
            None
        """
        raise NotImplementedError()

    def get_columns(self, table: str) -> list:
        """
        Get all static columns in a collection

        Args:
            table: str - collection name

        Returns:
            list
        """
        raise NotImplementedError()

    def get_indexes(self, table: str) -> list:
        """
        Get all indexes

        Args:
            table:str - collection name

        Returns:
            list
        """
        raise NotImplementedError()

    def get_collections(self) -> list:
        """
        Get all the collections in the DB

        Returns:
            list
        """
        raise NotImplementedError()

    def add_columns(self, table, cols_stmt: list):
        """
        Add columns into collection

        Args:
            table: str: table name
            cols_stmt: list - list of columns of to add in below format
                [
                    (col, coltype, index=bool|UNIQUE),
                    ....
                ]
        
        Returns:
            None
        """
        raise NotImplementedError()

    def get_size(self, table) -> int:
        """
        Get the total entries in the collection

        Args:
            table:str - Collection name
        Returns:
            int
        """
        return self.fetchone("SELECT COUNT(*) AS count FROM %s" % table)["count"]

    def fetchone(self, query: str, params: Any = {}) -> Any:
        """
        Fetch a single entry

        Args:
            query:str
            params: tuple
        
        Returns:
            dict 
        """
        cursor = self.execute(query=query, params=params)
        columns = [col[0] for col in cursor.description]
        res = cursor.fetchone()
        if res:
            return dict(zip(columns, res))
        return None

    def fetchall(self, query: str, params: Any = {}) -> Any:
        """
        Fetch all entries 

        Args:
            query:str
            params: tuple
        
        Returns:
            List[dict] 
        """
        cursor = self.execute(query=query, params=params)
        columns = [col[0] for col in cursor.description]
        res = cursor.fetchall()
        if not res:
            return []
        return [dict(zip(columns, row)) for row in res]

    def fetchmany(self, query: str, params: Any = {}, chunk: int = 100):
        """
        Fetch entries in chunk

        Args:
            query:str
            params: tuple
            chunck: int
        
        Returns:
            Yield[List[dict]] 
        """

        cursor = self.execute(query, params)
        columns = [col[0] for col in cursor.description]
        while True:
            chunked = cursor.fetchmany(chunk)
            if chunked:
                yield [dict(zip(columns, row)) for row in chunked]
            else:
                break


class SQLiteAdapter(Adapter):
    """
    SQLite Adapter
    
    SQLiteAdapter(":memory:")
    SQLiteAdapter("/file.db")
    SQLiteAdapter("sqlite://") - memory
    SQLiteAdapter("sqlite:///file.db") - file
    """

    _columns = []
    _indexes = []
    engine = "sqlite"

    def __init__(self, file: str = ":memory:"):
        if file in ["sqlite://"]:
            file = ":memory:"
        elif file.startswith("sqlite://"):
            _ = urlparse(file)
            file = _.path.strip("/") or None
        self.db = sqlite3.connect(file, isolation_level=None)
        self.db.execute('pragma journal_mode=wal')

    def execute(self, query, params={}):
        with self.db:
            return self.db.execute(query, params or {})

    def create_collection(self, table):
        q = "CREATE TABLE IF NOT EXISTS %s (_id VARCHAR(32) PRIMARY KEY, _json TEXT, _created_at TIMESTAMP  NOT NULL DEFAULT '0000-00-00 00:00:00', _modified_at TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00')" % table
        self.execute(q)

    def get_columns(self, table: str):
        if not self._columns:
            try:
                res = self.fetchall("PRAGMA table_info(%s)" % table)
                self._columns = [r["name"] for r in res]
            except Exception as e:
                pass
        return self._columns

    def get_indexes(self, table: str) -> list:
        """
        Get the list of all indexes

        Returns:
            list
        """
        if not self._indexes:
            try:
                indexes = []
                for item in self.fetchall("PRAGMA index_list(%s)" % table):
                    i2 = self.fetchone("PRAGMA index_info(%s)" % item["name"])
                    indexes.append(i2["name"])
                self._indexes = indexes
            except Exception as e:
                pass
        return self._indexes

    def get_collections(self) -> list:
        q = "SELECT name FROM sqlite_master WHERE type=?"
        res = self.fetchall(q, ('table', ))
        return [item["name"] for item in res]

    def add_columns(self, table, cols_stmt: list):
        columns = self.get_columns(table)
        indexes = self.get_indexes(table)
        for _ in cols_stmt:
            try:

                col, coltype, colindex = _

                # Add column if not exists
                if col not in columns:
                    self.execute("ALTER TABLE %s ADD COLUMN %s %s DEFAULT NULL" % (
                        table, col, coltype))

                # Add index if not exists
                if colindex and col not in indexes:
                    index_stmt = None
                    # unique
                    if isinstance(colindex, str) and colindex.upper() == "UNIQUE":
                        index_stmt = "UNIQUE"
                    # regular
                    elif colindex is True:
                        index_stmt = ""
                    if index_stmt is not None:
                        self.execute("CREATE %s INDEX %s ON %s (%s)" %
                                     (index_stmt, col+"__idx", table, col))
            except Exception as e:
                pass

        # reset columns
        self._columns = []
        self._indexes = []


class MySQLAdapter(Adapter):
    """
    MySQL Adapter 

    MySQLAdapter("mysql://user:password@host:port/dbname")
    """
    
    engine = "mysql"

    # Caching columns and indexes
    _columns = []
    _indexes = []

    type_converter = {
        "boolean": "TINYINT(1)",
        "text": "VARCHAR"
    }

    def __init__(self, dsn: str, autocommit=True):
        _ = urlparse(dsn)
        dbname = _.path.strip("/") or None
        config = {
            "host": _.hostname,
            "user": _.username,
            "password": _.password,
            "database": dbname,
            "port": _.port,
            "autocommit": autocommit
        }
        self.db = steady_db.connect(creator = pymysql, **config)

    def execute(self, query, params={}):
        with self.db.cursor() as cursor:
            # convert qmark for pymysql
            if params:
                query, params = convert_qmark_query_to_adapter_style(query, params, 'format')
            cursor.execute(query, params)
            return cursor
        
    def create_collection(self, table):
        self.execute("CREATE TABLE IF NOT EXISTS %s (_id VARCHAR(32) PRIMARY KEY, _json MEDIUMTEXT, _created_at DATETIME NOT NULL, _modified_at DATETIME NOT NULL)" % table)

    def get_columns(self, table: str) -> list:
        try:
            return [item["Field"] for item in self.fetchall("SHOW COLUMNS FROM %s" % table)]
        except Exception as e: 
            pass

    def get_indexes(self, table: str) -> list:
        try:
            return [item["Column_name"] for item in self.fetchall("SHOW INDEX FROM %s" % table)]
        except Exception as e: pass

    def get_collections(self) -> list:
        return [list(item.values())[0] for item in self.fetchall("SHOW TABLES")]

    def add_columns(self, table, cols_stmt: list):
        columns = self.get_columns(table)
        indexes = self.get_indexes(table)
        for _ in cols_stmt:
            try:

                col, coltype, colindex = _

                # Add column if not exists
                if col not in columns:
                    self.execute("ALTER TABLE %s ADD COLUMN %s %s DEFAULT NULL" % (table, col, coltype))

                # Add index if not exists
                if colindex and col not in indexes:
                    index_stmt = None
                    # unique
                    if isinstance(colindex, str) and colindex.upper() == "UNIQUE":
                        index_stmt = "UNIQUE"
                    # regular
                    elif colindex is True:
                        index_stmt = ""
                    if index_stmt is not None:
                        self.execute("CREATE %s INDEX %s ON %s (%s)" %
                                     (index_stmt, col+"__idx", table, col))
            except Exception as e:
                pass

        # reset columns
        self._columns = []
        self._indexes = []


