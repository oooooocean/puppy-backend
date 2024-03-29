# 流程
- 制定开发计划
- 确认开发计划: UI, 接口, 入参出参
- coding
- 自测
- 提交审核: 每两周做一个分享.

# 代码规范
- 除非是通用类, 否则文件名称和类名必须包含业务语义.
- 编辑, 展示业务逻辑不能耦合, 通过模板方法/继承来解决(或其他设计模式).

# 后端
- 用户主键的路径参数使用`int:user_id`.

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

### 2.3 命名
- 新增: add
- 编辑: edit

### 2.4 UI
- 浅底边框使用`borderColor`, 深色边框使用`greyColor`
- hint文案使用`greyColor`
- 浅色背景`backgroundColor`