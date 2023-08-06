create table if not exists ApiKey (
    id integer primary key autoincrement,
    name text not null unique,
    api_key blob not null,
    salt blob not null,
    creation_date datetime not null

);
