-- depends: 041__add_data_service_expose_block

alter table FilterBlockInput add column filter_selection_only integer not null default 0
