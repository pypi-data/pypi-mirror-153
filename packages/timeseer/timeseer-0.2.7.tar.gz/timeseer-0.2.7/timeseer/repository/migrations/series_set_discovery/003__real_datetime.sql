-- depends: 002__discovery_reason

update DiscoveryConfigurations set start_date = cast(strftime('%s', start_date) as real);
update DiscoveryConfigurations set end_date = cast(strftime('%s', end_date) as real);

update DiscoveryRuns set start_date = cast(strftime('%s', start_date) as real);
update DiscoveryRuns set end_date = cast(strftime('%s', end_date) as real);
