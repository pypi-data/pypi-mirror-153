-- depends: 012__add_metadata_audit_trail_type

update MetadataAuditTrails set modified_date = cast(strftime('%s', modified_date) as real);
