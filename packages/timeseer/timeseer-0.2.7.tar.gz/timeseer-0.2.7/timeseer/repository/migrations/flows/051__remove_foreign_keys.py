import sqlite3

from yoyo import step

__depends__ = {"049__alter_bad_actors"}


def remove_foreign_keys(db: sqlite3.Connection):
    cursor = db.cursor()
    cursor.execute("pragma schema_version")
    (schema_version,) = cursor.fetchone()
    cursor.execute("pragma writable_schema = ON")
    cursor.execute(
        """
        update sqlite_master
        set sql = 'CREATE TABLE FlowEvaluations (
    id integer primary key autoincrement,
    group_id integer not null,
    series_set_name text not null
)'
        where type = 'table' and name = 'FlowEvaluations'
    """
    )
    cursor.execute(f"pragma schema_version = {schema_version + 1}")
    cursor.execute("pragma writable_schema = OFF")


steps = [
    step(remove_foreign_keys),
]
