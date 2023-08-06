-- depends: 001__create

alter table DiscoveryRuns rename to DiscoveryRunsOld;

create table DiscoveryRuns (
    id integer primary key autoincrement,
    configuration_id integer not null,
    series_set_name text not null,
    reason text not null,
    start_date datetime not null,
    end_date datetime not null,

    unique (configuration_id, series_set_name, reason),
    foreign key (configuration_id) references DiscoveryConfigurations(id) on delete cascade
);

insert into DiscoveryRuns
select id, configuration_id, series_set_name, 'correlation', start_date, end_date
from DiscoveryRunsOld;

alter table DiscoveredSets rename to DiscoveredSetsOld;

create table DiscoveredSets (
    id integer primary key autoincrement,
    run_id integer not null,
    discovered_set_number integer not null,
    series_id text not null,

    foreign key (run_id) references DiscoveryRuns(id) on delete cascade
);

insert into DiscoveredSets
select * from DiscoveredSetsOld;

alter table ExistingSets rename to ExistingSetsOld;

create table ExistingSets (
    id integer primary key autoincrement,
    run_id integer not null,
    discovered_set_number integer not null,
    series_set_id integer,

    foreign key (run_id) references DiscoveryRuns(id) on delete cascade
);

insert into ExistingSets
select * from ExistingSets;

drop table DiscoveryRunsOld;
drop table DiscoveredSetsOld;
drop table ExistingSetsOld;
