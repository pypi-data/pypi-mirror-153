import json
import sqlite3

from yoyo import step

from timeseer.blocks import BlockType

__depends__ = {"045__remove_block_configurations"}


def update_blocks(db: sqlite3.Connection):
    cursor = db.cursor()
    _update_univariate_blocks(cursor)
    _update_univariate_block_evaluations(cursor)
    _update_multivariate_blocks(cursor)
    _update_multivariate_block_evaluations(cursor)


def _update_univariate_blocks(cursor: sqlite3.Cursor):
    cursor.execute(
        """
        select id, configuration
        from Blocks
        where type = ?
    """,
        [BlockType.UNIVARIATE_ANALYSIS.name],
    )
    for db_id, configuration in cursor.fetchall():
        new_configuration = _build_univariate_configuration(configuration)
        cursor.execute(
            """
            update Blocks
            set configuration = ?
            where id = ?
        """,
            [json.dumps(new_configuration), db_id],
        )


def _update_univariate_block_evaluations(cursor: sqlite3.Cursor):
    cursor.execute(
        """
        select id, configuration
        from BlockEvaluations
        where type = ?
    """,
        [BlockType.UNIVARIATE_ANALYSIS.name],
    )
    for db_id, configuration in cursor.fetchall():
        new_configuration = _build_univariate_configuration(configuration)
        cursor.execute(
            """
            update BlockEvaluations
            set configuration = ?
            where id = ?
        """,
            [json.dumps(new_configuration), db_id],
        )


def _build_univariate_configuration(configuration):
    configuration = json.loads(configuration)
    new_configuration = []
    for module_type in configuration["moduleTypes"]:
        if module_type == "metadata_bugs":
            new_configuration.append("metadata_statistics")
            if "metadata_checks" not in new_configuration:
                new_configuration.append("metadata_checks")
        elif module_type == "metadata_smells":
            if "metadata_checks" not in new_configuration:
                new_configuration.append("metadata_checks")
        elif module_type in ["univariate_bugs", "univariate_smells"]:
            if "univariate_checks" not in new_configuration:
                new_configuration.append("univariate_checks")
        else:
            new_configuration.append(module_type)
    configuration["moduleTypes"] = new_configuration
    return configuration


def _update_multivariate_blocks(cursor: sqlite3.Cursor):
    cursor.execute(
        """
        select id, configuration
        from Blocks
        where type = ?
    """,
        [BlockType.MULTIVARIATE_ANALYSIS.name],
    )
    for db_id, configuration in cursor.fetchall():
        new_configuration = _build_multivariate_configuration(configuration)
        cursor.execute(
            """
            update Blocks
            set configuration = ?
            where id = ?
        """,
            [json.dumps(new_configuration), db_id],
        )


def _update_multivariate_block_evaluations(cursor: sqlite3.Cursor):
    cursor.execute(
        """
        select id, configuration
        from BlockEvaluations
        where type = ?
    """,
        [BlockType.MULTIVARIATE_ANALYSIS.name],
    )
    for db_id, configuration in cursor.fetchall():
        new_configuration = _build_multivariate_configuration(configuration)
        cursor.execute(
            """
            update BlockEvaluations
            set configuration = ?
            where id = ?
        """,
            [json.dumps(new_configuration), db_id],
        )


def _build_multivariate_configuration(configuration):
    configuration = json.loads(configuration)
    new_configuration = []
    for module_type in configuration["moduleTypes"]:
        if module_type in ["multivariate_bugs", "multivariate_smells"]:
            if "multivariate_checks" not in new_configuration:
                new_configuration.append("multivariate_checks")
        else:
            new_configuration.append(module_type)
    configuration["moduleTypes"] = new_configuration
    return configuration


steps = [
    step(update_blocks),
]
