-- depends: 024__expose_block_pattern


alter table UnivariateBlockInput rename column block_id to block_configuration_id;
alter table MultivariateBlockInput rename column block_id to block_configuration_id;
alter table ExportBlockInput rename column block_id to block_configuration_id;
alter table FlightExposeBlockInput rename column block_id to block_configuration_id;
alter table TrendMinerExposeBlockInput rename column block_id to block_configuration_id;
alter table ComparisonBlockInput rename column block_id to block_configuration_id;
