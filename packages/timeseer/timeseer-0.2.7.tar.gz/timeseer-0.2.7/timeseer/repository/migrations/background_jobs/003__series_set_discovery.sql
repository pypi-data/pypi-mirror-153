-- depends: 002__add_start_end_date

update BackgroundJobs set name = 'series_set_discovery' where name = 'correlation_recommender';
