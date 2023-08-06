-- depends: 016__add_comparison_block

alter table BlockConfigurations add column name text;

alter table Blocks add column sort_order integer;


update BlockConfigurations set name = 'Univariate analysis'
where type = 'UNIVARIATE_ANALYSIS';
update BlockConfigurations set name = 'Multivariate analysis'
where type = 'MULTIVARIATE_ANALYSIS';
update BlockConfigurations set name = 'Report'
where type = 'REPORT';
update BlockConfigurations set name = 'Comparison'
where type = 'COMPARISON';
update BlockConfigurations set name = 'Filters'
where type = 'FILTER';
update BlockConfigurations set name = 'Export'
where type = 'EXPORT';
update BlockConfigurations set name = 'Expose as flight'
where type = 'FLIGHT_EXPOSE';

update Blocks set sort_order = id;
