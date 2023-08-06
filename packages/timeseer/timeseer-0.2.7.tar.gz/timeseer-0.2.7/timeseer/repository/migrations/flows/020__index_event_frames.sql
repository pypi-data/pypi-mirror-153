-- depends: 019__add_event_frame_reference

create index if not exists se_series_source on Series_EventFrame(series_source);
create index if not exists se_series_id on Series_EventFrame(series_id);
