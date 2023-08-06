import sqlite3

from yoyo import step

__depends__ = {"046__update_block_evaluations"}


def migrate_block_evaluations(db: sqlite3.Connection):
    cursor = db.cursor()
    cursor.execute("pragma schema_version")
    (schema_version,) = cursor.fetchone()
    cursor.execute("pragma writable_schema = ON")
    cursor.execute(
        """
        update sqlite_master
        set sql = 'CREATE TABLE BlockEvaluations (
    id integer primary key autoincrement,
    block_id integer,
    flow_evaluation_id integer not null,
    type text not null,
    name text not null,
    configuration text not null,
    sort_order integer not null,

    foreign key (flow_evaluation_id) references FlowEvaluations(id) on delete cascade
)'
        where type = 'table' and name = 'BlockEvaluations'
    """
    )
    cursor.execute(f"pragma schema_version = {schema_version + 1}")
    cursor.execute("pragma writable_schema = OFF")


steps = [
    step(migrate_block_evaluations),
]
