-- depends: 013__real_datetime

delete from MetadataAuditTrails where old_value is NULL and new_value is "";
