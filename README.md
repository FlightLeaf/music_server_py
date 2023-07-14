# Flask file server
用flask实现文件上传下载服务

### 上传服务
启动python app.py

访问地址http://127.0.0.1:8067/


### 下载服务（后面跟文件名称）
#### 方法一
访问地址http://127.0.0.1:8067/download/1.png

#### 方法二 用http.server
到需要下载的目录

python -m http.server
