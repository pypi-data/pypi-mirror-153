import sqlite3

from yoyo import step

__depends__ = {"052__update_flow_evaluation_groups"}


def add_foreign_keys(db: sqlite3.Connection):
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
    series_set_name text not null,
    foreign key (group_id) references FlowEvaluationGroups(id) on delete cascade
)'
        where type = 'table' and name = 'FlowEvaluations'
    """
    )
    cursor.execute(f"pragma schema_version = {schema_version + 1}")
    cursor.execute("pragma writable_schema = OFF")


steps = [
    step(add_foreign_keys),
]
