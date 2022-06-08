from django.db import models
from api.models.public.audit import AuditStatus


class AuditMixin(models.Model):
    audit_status = models.IntegerField('审核状态', choices=[(i.value, str(i)) for i in AuditStatus],
                                       default=AuditStatus.BLOCK.value)
    audit_description = models.CharField('审核意见', max_length=200, null=True, blank=True)

    class Meta:
        abstract = True

