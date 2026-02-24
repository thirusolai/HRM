"""
admin.py
"""

from django.contrib import admin

from kangaroo_audit.models import AuditTag, KangarooAuditInfo, KangarooAuditLog

# Register your models here.

admin.site.register(AuditTag)
