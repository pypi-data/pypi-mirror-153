-- depends: 001__create

update ApiKey set creation_date = cast(strftime('%s', creation_date) as real);
