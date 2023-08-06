-- depends: 006__rename_to_blocks

create index fe_flow_id on FlowEvaluations(flow_id);

create index filter_output_fe_id on FilterBlockOutput(flow_evaluation_id);
create index seriesset_output_fe_id on SeriesSetBlockOutput(flow_evaluation_id);

create index bivariate_fe_id on BivariateChecks(flow_evaluation_id);
create index calculated_metadata_fe_id on CalculatedMetadata(flow_evaluation_id);
create index checks_fe_id on Checks(flow_evaluation_id);
create index eventframes_fe_id on EventFrames(flow_evaluation_id);
create index series_eventframes_eventframe_id on Series_EventFrame(event_frame_id);
create index bivariate_eventframes_eventframe_id on BivariateCheck_EventFrame(event_frame_id);
create index statistics_fe_id on Statistics(flow_evaluation_id);

create index exports_fe_id on Exports(flow_evaluation_id);
create index scores_fe_id on Scores(flow_evaluation_id);
