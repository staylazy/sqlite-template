import sqlite3
import os
from typing import Dict, Tuple, List


conn = sqlite3.connect(os.path.join('info.db'))
cursor = conn.cursor()

def delete(table: str, line_id: int):
    cursor.execute(f"delete from {table} where id={line_id}")
    conn.commit()

def insert(table: str, column_values: Dict):
    columns = ', '.join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ', '.join("?" * len(column_values.keys()))
    cursor.executemany(
        f"INSERT INTO {table} "
        f"({columns})"
        F"VALUES ({placeholders})",
        values
    )
    conn.commit()

def _init_db():
    with open(os.path.join('create_database.sql'), 'r') as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()        

def get_cursor():
    return cursor

def check_db_existance():
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='laundry_queue'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()

def fetchall(table: str, columns: List[str]) -> List[Tuple]:
    columns_joined = ', '.join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table}")
    lines = cursor.fetchall()
    result = []
    for line in lines: 
        dict_line = {}
        for i, col in enumerate(columns):
            dict_line[col] = line[i]
        result.append(dict_line)
    return result

check_db_existance()
