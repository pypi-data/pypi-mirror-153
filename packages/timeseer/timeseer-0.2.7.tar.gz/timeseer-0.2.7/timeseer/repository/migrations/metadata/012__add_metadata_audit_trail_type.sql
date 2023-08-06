-- depends: 010__rename_limits

alter table MetadataAuditTrails add column type text default 'SOURCE';

delete from MetadataAuditTrails;
