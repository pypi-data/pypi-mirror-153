import sqlite3

from yoyo import step

__depends__ = {"015__add_tags_field"}


def add_foreign_keys(db: sqlite3.Connection):
    cursor = db.cursor()
    cursor.execute("pragma schema_version")
    (schema_version,) = cursor.fetchone()
    cursor.execute("pragma writable_schema = ON")
    cursor.execute(
        """
        update sqlite_master
        set sql = 'create table SeriesTags (
    id integer primary key autoincrement,
    series_id text not null,
    tag_key text not null,
    tag_value text not null,

    unique(series_id, tag_key, tag_value),
    foreign key (series_id) references SeriesNames(series_id) on delete cascade
)'
        where type = 'table' and name = 'SeriesTags'
    """
    )
    cursor.execute(f"pragma schema_version = {schema_version + 1}")
    cursor.execute("pragma writable_schema = OFF")


steps = [
    step(add_foreign_keys),
]
