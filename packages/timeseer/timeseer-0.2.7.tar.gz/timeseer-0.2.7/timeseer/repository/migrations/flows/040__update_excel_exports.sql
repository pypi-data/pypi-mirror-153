-- depends: 039__excel_exports

alter table ExcelExports rename to old_ExcelExports;

create table ExcelExports (
    id integer primary key autoincrement,
    block_evaluation_id integer not null,
    series_id text not null,
    filename text,
    file blob,
    date datetime,
    type text,
    start_date datetime,
    end_date datetime,

    foreign key (block_evaluation_id) references BlockEvaluations(id) on delete cascade
);


create table ExcelExport_EventFrames (
    id integer primary key autoincrement,
    excel_export_id int not null,
    frame_type text not null,

    foreign key (excel_export_id) references ExcelExports(id) on delete cascade
);

drop table old_ExcelExports;
drop table Series_ExcelExports;
drop table Series_ExcelExport_EventFrames;
