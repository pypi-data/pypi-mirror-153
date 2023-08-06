-- depends: 001__create

drop table CompressionOptimizationResults;

drop table CompressionOptimizations;

create table CompressionOptimizations(
    id integer primary key autoincrement,
    series_id text not null,
    start_date datetime not null,
    end_date datetime not null,

    unique (series_id)
);

create table CompressionOptimizationResults(
    id integer primary key autoincrement,
    optimization_id integer not null,
    exception_deviation real not null,
    compression_deviation real not null,
    mutual_information real not null,
    compression_ratio real not null,


    foreign key (optimization_id) references CompressionOptimizations(id) on delete cascade
);
