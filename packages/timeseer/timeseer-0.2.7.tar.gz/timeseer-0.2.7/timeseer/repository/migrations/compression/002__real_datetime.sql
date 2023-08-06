-- depends: 001__create

update CompressionOptimizations set start_date = cast(strftime('%s', start_date) as real);
update CompressionOptimizations set end_date = cast(strftime('%s', end_date) as real);
