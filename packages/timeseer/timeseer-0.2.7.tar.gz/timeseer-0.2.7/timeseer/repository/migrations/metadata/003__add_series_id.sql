-- depends: 002__add_table_metadata_state

create table SeriesNames(
    series_id text primary key,
    series_source text not null,
    series_name text not null,

    unique(series_source, series_name)
)
