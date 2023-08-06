-- depends: 002__kpis
alter table WeightSets add column origin text not null default "default";

create table WeightSetKPIs (
    id integer primary key autoincrement,
    weight_set_id integer not null,
    kpi_id text not null,

    unique(weight_set_id, kpi_id)
    foreign key (weight_set_id) references WeightSets(id) on delete cascade,
    foreign key (kpi_id) references KPIs(id) on delete cascade
);