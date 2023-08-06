-- depends: 028__change_module_types

update CalculatedMetadata set field_name = 'functional lower limit' where field_name = 'lower limit';
update CalculatedMetadata set field_name = 'functional upper limit' where field_name = 'upper limit';
