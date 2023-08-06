
create table DiscoveryConfigurations (
    id integer primary key autoincrement,
    template_id integer not null,
    start_date datetime,
    end_date datetime,
    relative_date text
);

create table DiscoveryRuns (
    id integer primary key autoincrement,
    configuration_id integer not null,
    series_set_name text not null,
    start_date datetime not null,
    end_date datetime not null,

    unique (configuration_id, series_set_name)
    foreign key (configuration_id) references DiscoveryConfigurations(id) on delete cascade
);

create table DiscoveredSets (
    id integer primary key autoincrement,
    run_id integer not null,
    discovered_set_number integer not null,
    series_id text not null,

    foreign key (run_id) references DiscoveryRuns(id) on delete cascade
);

create table ExistingSets (
    id integer primary key autoincrement,
    run_id integer not null,
    discovered_set_number integer not null,
    series_set_id integer,

    foreign key (run_id) references DiscoveryRuns(id) on delete cascade
);

create table ScheduledDiscoveryConfigurations (
    id integer primary key autoincrement,
    configuration_id integer not null unique,
    schedule_interval text not null,

    foreign key (configuration_id) references DiscoveryConfigurations(id) on delete cascade
);
