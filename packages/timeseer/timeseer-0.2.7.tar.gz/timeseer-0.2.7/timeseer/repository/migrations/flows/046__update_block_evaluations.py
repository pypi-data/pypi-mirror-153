import sqlite3

from yoyo import step

__depends__ = {"045__remove_block_configurations"}


def update_block_evaluations(db: sqlite3.Connection):
    cursor = db.cursor()
    cursor.executescript(
        """
        alter table BlockEvaluations add column type text;
        alter table BlockEvaluations add column name text;
        alter table BlockEvaluations add column configuration text;
        alter table BlockEvaluations add column sort_order integer;

        create unique index block_evaluations_fe_name on BlockEvaluations(flow_evaluation_id, name);
    """
    )

    cursor.execute("select id, block_id from BlockEvaluations")
    for block_evaluation_id, block_id in cursor.fetchall():
        cursor.execute(
            """
            select type, name, configuration, sort_order
            from Blocks
            where id = ?
        """,
            [block_id],
        )
        block_type, name, configuration, sort_order = cursor.fetchone()
        cursor.execute(
            """
            update BlockEvaluations
            set
                type = ?,
                name = ?,
                configuration = ?,
                sort_order = ?
            where id = ?
        """,
            [block_type, name, configuration, sort_order, block_evaluation_id],
        )


steps = [
    step(update_block_evaluations),
]
