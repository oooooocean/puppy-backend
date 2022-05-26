# 后端
- 用户主键的路径参数使用`int:user_id`

# 前端
## 1. 请求
- 局部更新使用`PATCH`, 新建使用`POST`, `Content-Type`使用`application/json`
- 分页页码从1开始, 使用size(可选)和page定义参数.
- 请求的`Accept`字段使用`application/json`.

## 2. 图片处理
### 2.1 图片处理
- app图片缓存策略需要设置为硬盘缓存.
- 图片格式为`JPEG`.
- 图片在上传前需要进行压缩, 压缩目标值为当前市面上最大手机屏幕的像素值.
- 图片名称格式为`<user_id>/<uuid>.jpeg`

### 2.2 图片使用
```
// 样式名称: thumbnail200x200.AspectFill
// 缩略图: 200px*200px
// 资源格式: 1649381392401571261710336.jpeg-thumbnail200x200.AspectFill
http://rcgvzdinm.hd-bkt.clouddn.com/1649381392401571261710336.jpeg-thumbnail200x200.AspectFill

// 自动优化展示:
http://rcgvzdinm.hd-bkt.clouddn.com/1649381392401571261710336.jpeg?imageslim

// 自定义展示:
// w和h可以只传1个
http://rcgvzdinm.hd-bkt.clouddn.com/1649381392401571261710336.jpeg?imageView2/0/w/200/h/200/ignore-error/1
```

### 2.3 安全策略
- 对上传或修改动作, 需要确认请求方是否拥有修改或删除的权限. 使用上传凭证、下载凭证和管理凭证来确认权限.
- 客户端上传前需要先获取从服务端颁发的上传凭证, 并在上传资源时将上传凭证包含为请求内容的一部分.
- 