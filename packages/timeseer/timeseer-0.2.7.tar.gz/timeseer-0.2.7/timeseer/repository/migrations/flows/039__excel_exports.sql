-- depends: 038__create_quadrant_scores

create table ExcelExporterRuns (
    id integer primary key autoincrement,
    excel_export_id int not null,
    state text not null,

    unique(excel_export_id)
);

create table ExcelExports (
    id integer primary key autoincrement,
    block_evaluation_id integer not null,
    filename text,
    file blob,
    date datetime,
    type text,

    foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade
);

create table Series_ExcelExports (
    id integer primary key autoincrement,
    excel_export_id not null,
    series_source text not null,
    series_id text not null,
    start_date datetime,
    end_date datetime,

    foreign key (excel_export_id) references ExcelExports(id) on delete cascade
);

create table Series_ExcelExport_EventFrames (
    id integer primary key autoincrement,
    series_excel_export_id int not null,
    frame_type text not null,

    foreign key (series_excel_export_id) references Series_ExcelExports(id) on delete cascade
);
