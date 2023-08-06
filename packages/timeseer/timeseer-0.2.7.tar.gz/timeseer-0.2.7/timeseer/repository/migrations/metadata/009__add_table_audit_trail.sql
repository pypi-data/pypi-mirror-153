-- depends: 007__add_series_block_id

create table if not exists MetadataAuditTrails (
    id integer primary key autoincrement,
    source_name text not null,
    series_id text not null,
    field_name text not null,
    old_value text,
    new_value text,
    modified_date datetime not null
);
