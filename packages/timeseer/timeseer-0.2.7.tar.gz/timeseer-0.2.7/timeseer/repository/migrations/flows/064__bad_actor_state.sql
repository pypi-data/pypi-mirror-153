-- depends: 063__replace_min

alter table UnivariateBadActorScore add column state text not null default 'smell';

update UnivariateBadActorScore set state = 'ok' where score = 0.0;
update UnivariateBadActorScore set state = 'bug' where score = 1.0;