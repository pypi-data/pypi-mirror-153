-- depends: 004__create_series_set_metadata

alter table SeriesSet add column origin text;
alter table SeriesSetTemplates add column origin text not null default 'ui';
