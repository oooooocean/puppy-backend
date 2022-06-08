from enum import IntEnum


class AuditStatus(IntEnum):
    SUCCESS = 0
    BLOCK = 1  # 正在等待审核
    FAIL = 2

    def __str__(self):
        return ['审核成功', '审核中', '审核失败'][self.value]
