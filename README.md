# flask_bbs
### 模仿cnode论坛用flask实现的一个论坛
- 论坛实现了用户**注册、登陆、上传头像、发表文章、评论、私信**等功能
- 对用户密码使用**SHA256**并加盐处理
- 使用**MongoDB**存储数据并实现相应的**ORM**
- 利用**jinja2**模板实现网页模板，**解耦**页面与业务逻辑，提高代码重用度
- 使用**Nginx**反向代理，处理静态文件，同时配合**gunicorn**实现多进程的负载均衡
- 利用**Python uuid**模块生成随机数防范**CSRF**攻击

论坛首页如下图:
![](https://github.com/TechManiaTC/flask_bbs/blob/master/static/bbs.png)
