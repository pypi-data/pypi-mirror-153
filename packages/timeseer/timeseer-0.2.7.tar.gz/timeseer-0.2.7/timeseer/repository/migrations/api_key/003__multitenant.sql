-- depends: 002__real_datetime

create table ApiKeys (
    id integer primary key autoincrement,
    tenant_id text not null,
    name text not null,
    api_key blob not null,
    salt blob not null,
    creation_date datetime not null,

    unique(tenant_id, name)
);

insert into ApiKeys
select id, '', name, api_key, salt, creation_date
from ApiKey;

drop table ApiKey;
