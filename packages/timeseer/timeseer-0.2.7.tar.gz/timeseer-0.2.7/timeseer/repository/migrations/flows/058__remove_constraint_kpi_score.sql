-- depends: 056__rename_quarant_scores 057__change_module_types

create table new_FavoriteKPIScores(
    id integer primary key autoincrement,
    block_evaluation_id integer not null,
    name text not null,
    score real,

    unique(block_evaluation_id, name, score)
    foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade
);

insert into new_FavoriteKPIScores (id, block_evaluation_id, name, score)
select id, block_evaluation_id, name, score from FavoriteKPIScores;

drop table FavoriteKPIScores;

alter table new_FavoriteKPIScores rename to FavoriteKPIScores;

create index kpi_score_be_id on FavoriteKPIScores(block_evaluation_id);
