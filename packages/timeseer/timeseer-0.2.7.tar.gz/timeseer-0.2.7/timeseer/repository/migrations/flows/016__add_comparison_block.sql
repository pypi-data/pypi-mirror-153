-- depends: 015__add_trendminer_expose_block

create table ComparisonBlockInput (
    id integer primary key autoincrement,
    block_id integer not null,
    reference_start_date datetime not null,
    reference_end_date datetime not null,

    foreign key (block_id) references BlockConfigurations(id) on delete cascade
);
