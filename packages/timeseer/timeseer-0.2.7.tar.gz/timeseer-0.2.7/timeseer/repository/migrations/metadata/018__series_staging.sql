-- depends: 017__series_staging

drop table SeriesNamesStaging;

create table SeriesStagingFilter (
    batch_id integer not null,
    temp_id integer not null,
    series_representation text not null
);

create table SeriesStaging (
    batch_id integer not null,
    temp_id integer,
    series_source text not null,
    series_representation text not null,

    unique(series_source, series_representation),
    unique(batch_id, series_representation)
);
