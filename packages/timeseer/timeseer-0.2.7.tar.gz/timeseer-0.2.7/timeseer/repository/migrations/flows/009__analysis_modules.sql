-- depends: 008__blocks_refer_to_configurations

drop table UnivariateBlockInput;

create table UnivariateBlockInput (
    id integer primary key autoincrement,
    block_id integer not null,
    module_type text not null,

    foreign key (block_id) references BlockConfigurations(id) on delete cascade
);

insert into UnivariateBlockInput (block_id, module_type)
select id, 'metadata_metrics'
from BlockConfigurations
where type = 'UNIVARIATE_ANALYSIS';

insert into UnivariateBlockInput (block_id, module_type)
select id, 'metadata_indicators'
from BlockConfigurations
where type = 'UNIVARIATE_ANALYSIS';

insert into UnivariateBlockInput (block_id, module_type)
select id, 'univariate_statistics'
from BlockConfigurations
where type = 'UNIVARIATE_ANALYSIS';

insert into UnivariateBlockInput (block_id, module_type)
select id, 'univariate_metrics'
from BlockConfigurations
where type = 'UNIVARIATE_ANALYSIS';

insert into UnivariateBlockInput (block_id, module_type)
select id, 'univariate_indicators'
from BlockConfigurations
where type = 'UNIVARIATE_ANALYSIS';

insert into UnivariateBlockInput (block_id, module_type)
select id, 'regime_detection'
from BlockConfigurations
where type = 'UNIVARIATE_ANALYSIS';

drop table MultivariateBlockInput;

create table MultivariateBlockInput (
    id integer primary key autoincrement,
    block_id integer not null,
    module_type text not null,

    foreign key (block_id) references BlockConfigurations(id) on delete cascade
);

insert into MultivariateBlockInput (block_id, module_type)
select id, 'multivariate_statistics'
from BlockConfigurations
where type = 'MULTIVARIATE_ANALYSIS';

insert into MultivariateBlockInput (block_id, module_type)
select id, 'multivariate_metrics'
from BlockConfigurations
where type = 'MULTIVARIATE_ANALYSIS';

insert into MultivariateBlockInput (block_id, module_type)
select id, 'multivariate_indicators'
from BlockConfigurations
where type = 'MULTIVARIATE_ANALYSIS';
