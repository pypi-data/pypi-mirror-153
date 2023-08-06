-- depends: 027__series_name

update UnivariateBlockInput set module_type = 'metadata_smells' where module_type = 'metadata_indicators';
update UnivariateBlockInput set module_type = 'metadata_bugs' where module_type = 'metadata_metrics';
update UnivariateBlockInput set module_type = 'univariate_smells' where module_type = 'univariate_indicators';
update UnivariateBlockInput set module_type = 'univariate_bugs' where module_type = 'univariate_metrics';


update MultivariateBlockInput set module_type = 'multivariate_smells' where module_type = 'multivariate_indicators';
update MultivariateBlockInput set module_type = 'multivariate_bugs' where module_type = 'multivariate_metrics';
