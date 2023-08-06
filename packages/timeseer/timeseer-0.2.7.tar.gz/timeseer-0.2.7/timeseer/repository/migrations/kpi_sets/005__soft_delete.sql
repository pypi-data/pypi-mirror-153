-- depends: 004__kpi_help_text

alter table KPIs add column removed integer not null default 0;
alter table WeightSets add column removed integer not null default 0;