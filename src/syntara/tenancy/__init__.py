"""
Tenant-aware configuration and policies for Syntara.

This package currently defines a TenantPolicy and an in-memory TenantPolicyStore.
The store is not yet wired into core engines; it can be used by future
integration layers (e.g. API startup, admin console) to decide which rules
or thresholds apply to a given tenant.
"""
