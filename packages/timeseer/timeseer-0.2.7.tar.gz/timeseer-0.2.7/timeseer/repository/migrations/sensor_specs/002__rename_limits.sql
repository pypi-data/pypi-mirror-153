-- depends: 001__create

update SensorSpecs set field_name = 'functional lower limit' where field_name = 'lower limit';
update SensorSpecs set field_name = 'functional upper limit' where field_name = 'upper limit';
