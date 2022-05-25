# 后端
- 用户主键的路径参数使用`int:user_id`

# 前端
- 局部更新使用`PATCH`, 新建使用`POST`, `Content-Type`使用`application/json`
- 分页页码从1开始, 使用size(可选)和page定义参数.
- 请求的`Accept`字段使用`application/json`