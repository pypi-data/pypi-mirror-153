
create table ResourceInconsistencies(
    id integer primary key autoincrement,
    resource_name text not null,
    resource_type text not null,
    inconsistency text not null
);