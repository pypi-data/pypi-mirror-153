create table UnivariateHeatmapScore (
    id integer primary key autoincrement,
    block_evaluation_id integer not null,
    series_id text not null,
    start_date datetime not null,
    end_date datetime not null,
    score real not null,

    foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade
);
