--- depends: 047__add_block_evaluation_constraints

create index univariate_event_frames_be_series_id on UnivariateEventFrames(block_evaluation_id, flow_evaluation_series_id);
