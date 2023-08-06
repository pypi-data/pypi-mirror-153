-- depends: 009__add_table_audit_trail

update Metadata set field_name = 'functional lower limit' where field_name = 'lower limit';
update Metadata set field_name = 'functional upper limit' where field_name = 'upper limit';

update MetadataAuditTrails set field_name = 'functional lower limit' where field_name = 'lower limit';
update MetadataAuditTrails set field_name = 'functional upper limit' where field_name = 'upper limit';
