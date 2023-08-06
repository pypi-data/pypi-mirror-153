import sqlite3

from yoyo import step

__depends__ = {"065__check_conditions"}


def remove_foreign_keys(db: sqlite3.Connection):
    cursor = db.cursor()
    cursor.execute("pragma schema_version")
    (schema_version,) = cursor.fetchone()
    cursor.execute("pragma writable_schema = ON")
    cursor.execute(
        """
        update sqlite_master
        set sql = 'CREATE TABLE UnivariateSeriesState (
    id integer primary key autoincrement,
    block_evaluation_id integer not null,
    flow_evaluation_series_id integer not null,

    unique(block_evaluation_id, flow_evaluation_series_id),
    foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade
)'
        where type = 'table' and name = 'UnivariateSeriesState'
    """
    )
    cursor.execute(
        """
        update sqlite_master
        set sql = 'CREATE TABLE BivariateEventFrames (
    id integer primary key autoincrement,
    flow_evaluation_series_x_id text not null,
    flow_evaluation_series_y_id text not null,
    block_evaluation_id integer not null,

    type_id integer not null,
    start_date datetime not null,
    end_date datetime,

    foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade,
    foreign key (type_id) references EventFrameTypes(id) on delete no action,

    unique (block_evaluation_id, flow_evaluation_series_x_id, flow_evaluation_series_y_id, type_id, start_date)
)'
        where type = 'table' and name = 'BivariateEventFrames'
    """
    )
    cursor.execute(
        """
        update sqlite_master
        set sql = 'CREATE TABLE UnivariateEventFrames (
    id integer primary key autoincrement,
    flow_evaluation_series_id integer not null,
    block_evaluation_id integer not null,

    type_id integer not null,
    start_date datetime not null,
    end_date datetime,

    foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade,
    foreign key (type_id) references EventFrameTypes(id) on delete no action,

    unique (block_evaluation_id, flow_evaluation_series_id, type_id, start_date)
)'
        where type = 'table' and name = 'UnivariateEventFrames'
    """
    )
    cursor.execute(f"pragma schema_version = {schema_version + 1}")
    cursor.execute("pragma writable_schema = OFF")


steps = [
    step(remove_foreign_keys),
]
