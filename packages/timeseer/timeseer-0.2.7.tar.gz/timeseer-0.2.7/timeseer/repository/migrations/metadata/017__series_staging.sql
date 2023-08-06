-- depends: 016__add_foreign_keys

create table SeriesNamesStaging (
    batch_id integer not null,
    temp_id integer,
    series_source text,
    series_tag_keys text,
    series_tag_values text,
    series_field text
);

create table NewMetadataAuditTrails (
    batch_id integer not null,
    source_name text not null,
    series_id text not null,
    field_name text not null,
    old_value text,
    new_value text,
    modified_date datatime not null
);

create table RecentMetadataAuditTrails (
    batch_id integer not null,
    id integer not null,
    series_id text not null,
    field_name text not null,
    new_value text,
    type text,
    modified_date datatime not null
);
