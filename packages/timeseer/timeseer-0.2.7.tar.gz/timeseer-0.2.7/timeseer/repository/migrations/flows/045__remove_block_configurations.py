import json
import sqlite3

from typing import Callable

from yoyo import step

from timeseer.blocks import BlockConfiguration, BlockType
from timeseer.blocks.comparison import ComparisonBlock
from timeseer.blocks.data_service_expose import DataServiceExposeBlock
from timeseer.blocks.exports import ExportBlock
from timeseer.blocks.filters import (
    AugmentationStrategy,
    FilterBlock,
    FlowEventFrameFilter,
)
from timeseer.blocks.flight_expose import FlightExposeBlock
from timeseer.blocks.multivariate import MultivariateAnalysisBlock
from timeseer.blocks.trendminer_expose import TrendMinerExposeBlock
from timeseer.blocks.univariate import UnivariateAnalysisBlock
from timeseer.time_ranges import AbsoluteTimeRange


__depends__ = {"044__remove_evaluation_block_fk"}


def migrate_blocks(db: sqlite3.Connection):
    cursor = db.cursor()
    cursor.execute(
        """
        select b.id, b.flow_id, b.sort_order, c.id, c.name, c.type
        from Blocks b, BlockConfigurations c
        where b.configuration_id = c.id
    """
    )

    configuration_fns: dict[
        BlockType, Callable[[sqlite3.Cursor, int], BlockConfiguration]
    ] = {
        BlockType.COMPARISON: get_comparison_block,
        BlockType.DATA_SERVICE_EXPOSE: get_data_service_expose_block,
        BlockType.EXPORT: get_export_block,
        BlockType.FILTER: get_filter_block,
        BlockType.FLIGHT_EXPOSE: get_flight_expose_block,
        BlockType.MULTIVARIATE_ANALYSIS: get_multivariate_block,
        BlockType.TRENDMINER_EXPOSE: get_trendminer_expose_block,
        BlockType.UNIVARIATE_ANALYSIS: get_univariate_block,
    }

    for (
        block_id,
        flow_id,
        sort_order,
        configuration_id,
        block_name,
        block_type,
    ) in cursor.fetchall():
        configuration = configuration_fns[BlockType[block_type]](
            cursor, configuration_id
        )
        effective_name = block_name
        counter = 0
        while True:
            try:
                cursor.execute(
                    """
                    insert into Blocks_new (id, flow_id, type, name, configuration, sort_order)
                    values (?, ?, ?, ?, ?, ?)
                """,
                    [
                        block_id,
                        flow_id,
                        block_type,
                        effective_name,
                        json.dumps(configuration.to_data()),
                        sort_order,
                    ],
                )
                break
            except sqlite3.IntegrityError as err:
                counter = counter + 1
                if counter > 5:
                    raise err
                effective_name = f"{block_name} ({counter})"


steps = [
    step(
        """
            create table Blocks_new (
                id integer primary key autoincrement,
                flow_id integer not null,
                type text not null,
                name text not null,
                configuration text not null,
                sort_order integer not null,

                unique (flow_id, name),
                foreign key (flow_id) references Flows(id) on delete cascade
            );
        """,
    ),
    step(migrate_blocks),
    step("drop table Blocks"),
    step("alter table Blocks_new rename to Blocks"),
    step(
        """
            create table FlowDataService_new (
                id integer primary key autoincrement,
                name text not null unique,
                block_evaluation_id integer not null,
                flow_id integer not null,
                series_set_name text,
                block_name text not null,

                foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade,
                foreign key (flow_id) references Flows(id) on delete cascade
            );
    """
    ),
    step(
        """
        insert into FlowDataService_new (id, name, block_evaluation_id, flow_id, series_set_name, block_name)
        select d.id, d.name, d.block_evaluation_id, d.flow_id, d.series_set_name, c.name
    from FlowDataService d, BlockConfigurations c
        where d.block_configuration_id = c.id
    """
    ),
    step("drop table FlowDataService"),
    step("alter table FlowDataService_new rename to FlowDataService"),
    step(
        """
            create table FlowSource_new (
                id integer primary key autoincrement,
                flow_id integer not null,
                series_set_name text not null,
                block_name text not null,
                block_evaluation_id integer not null,
                name text not null unique,

                foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade,
                foreign key (flow_id) references Flows(id) on delete cascade
            );
    """
    ),
    step(
        """
        insert into FlowSource_new (id, name, block_evaluation_id, flow_id, series_set_name, block_name)
        select f.id, f.name, f.block_evaluation_id, f.flow_id, f.series_set_name, c.name
        from FlowSource f, BlockConfigurations c
        where f.block_configuration_id = c.id
    """
    ),
    step("drop table FlowSource"),
    step("alter table FlowSource_new rename to FlowSource"),
    step("drop table BlockConfigurations"),
    step("drop table ComparisonBlockInput"),
    step("drop table DataServiceExposeBlockInput"),
    step("drop table ExportBlockInput"),
    step("drop table FilterBlockInput"),
    step("drop table FlightExposeBlockInput"),
    step("drop table MultivariateBlockInput"),
    step("drop table TrendMinerExposeBlockInput"),
    step("drop table UnivariateBlockInput"),
]


def get_comparison_block(
    cursor: sqlite3.Cursor, block_configuration_id: int
) -> ComparisonBlock:
    """get the comparison block."""
    cursor.execute(
        """
        select reference_start_date, reference_end_date from ComparisonBlockInput
        where block_configuration_id = ?
    """,
        [block_configuration_id],
    )
    reference_start_date, reference_end_date = cursor.fetchone()
    return ComparisonBlock(AbsoluteTimeRange(reference_start_date, reference_end_date))


def get_data_service_expose_block(
    cursor: sqlite3.Cursor, block_configuration_id: int
) -> DataServiceExposeBlock:
    """Get the data service expose block."""
    cursor.execute(
        """
        select pattern from DataServiceExposeBlockInput
        where block_configuration_id = ?
    """,
        [block_configuration_id],
    )
    (pattern,) = cursor.fetchone()
    return DataServiceExposeBlock(pattern)


def get_export_block(
    cursor: sqlite3.Cursor, block_configuration_id: int
) -> ExportBlock:
    """get the report block."""
    cursor.execute(
        """
        select export from ExportBlockInput
        where block_configuration_id = ?
    """,
        [block_configuration_id],
    )
    exports = [export for export, in cursor]
    return ExportBlock(exports)


def get_filter_block(
    cursor: sqlite3.Cursor, block_configuration_id: int
) -> FilterBlock:
    """get the filter block."""
    cursor.execute(
        """
        select frame_type, frame_type_category, augmentation_strategy, series_id, filter_selection_only
        from FilterBlockInput
        where block_id = ?
    """,
        [block_configuration_id],
    )
    filters = []
    augmentation_strategy = None
    for (
        frame_type,
        frame_type_category,
        strategy,
        series_id,
        filter_selection_only,
    ) in cursor:
        augmentation_strategy = AugmentationStrategy[strategy]
        filters.append(
            FlowEventFrameFilter.from_string(
                frame_type,
                frame_type_category,
                series_id,
                bool(filter_selection_only),
            )
        )
    return FilterBlock(filters, augmentation_strategy)


def get_flight_expose_block(
    cursor: sqlite3.Cursor, block_configuration_id: int
) -> FlightExposeBlock:
    """Return a flight expose block."""
    cursor.execute(
        """
        select pattern from FlightExposeBlockInput
        where block_configuration_id = ?
    """,
        [block_configuration_id],
    )
    (pattern,) = cursor.fetchone()
    return FlightExposeBlock(pattern)


def get_multivariate_block(
    cursor: sqlite3.Cursor, block_configuration_id: int
) -> MultivariateAnalysisBlock:
    """get the multivariate analysis block."""
    cursor.execute(
        """
        select module_type from MultivariateBlockInput
        where block_configuration_id = ?
    """,
        [block_configuration_id],
    )
    module_types = [module_type for module_type, in cursor]
    return MultivariateAnalysisBlock(module_types, [], {})


def get_trendminer_expose_block(
    cursor: sqlite3.Cursor, block_configuration_id: int
) -> TrendMinerExposeBlock:
    """get the TrendMiner expose block."""
    cursor.execute(
        """
        select name, prefix from TrendMinerExposeBlockInput
        where block_configuration_id = ?
    """,
        [block_configuration_id],
    )
    name, prefix = cursor.fetchone()
    return TrendMinerExposeBlock(name, prefix)


def get_univariate_block(
    cursor: sqlite3.Cursor, block_configuration_id: int
) -> UnivariateAnalysisBlock:
    """get the univariate block."""
    cursor.execute(
        """
        select module_type from UnivariateBlockInput
        where block_configuration_id = ?
    """,
        [block_configuration_id],
    )
    module_types = [module_type for module_type, in cursor]
    return UnivariateAnalysisBlock(module_types, [], {})
