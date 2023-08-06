-- depends: 062__soft_delete_groups

update Statistics set statistic_result = replace(statistic_result, "min", "m") where statistic_name = "Interpolation information loss";
update Statistics set statistic_name = replace(statistic_name, "min", "m") where statistic_name like "Interpolation information loss%";