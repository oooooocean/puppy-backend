### 1. Model 权限设计
条件A: 登录用户和路径参数标记的用户一致
条件B: model属于路径参数标记的用户

- `GET /user/A/pets/`: 条件B, 列表, 属于用户A的所有宠物
- `GET /user/A/pets/B`: 无条件, 详情, B是A的宠物, 不需要验证A是不是当前用户的
- `POST /user/A/pets/`: 条件A & 条件B, 新建, 为用户A创建新宠物, 且A是当前用户
- `PATCH /user/A/pets/B`: 条件A & 条件B, 更新, B是A的宠物, 且A必须是当前登录用户
- `DELETE /user/A/pets/B`: 条件A & 条件B, 删除