-- depends: 005__add_series_removed

create index if not exists sn_series_source on SeriesNames(series_source);
