<div align="center">

<h1 align="center">Ai-applet</h1>

简体中文 / [English](./README_EN.md)

Image generation using stable diffusion, multi-cluster, task scheduling center.

利用stable diffusion 生成图像，多集群，任务调度中台。

</div>

## 特点

- 利用stable diffusion 生成图像，支持多机器，自动调度。
- 开发逻辑清晰，不改stable diffusion 源码，支持自定义模型，支持多集群，支持多任务，支持多用户。
- 使用DRF构建API，代码逻辑简单，上手难度低。
- 支持oss上传，减少带宽压力。
- 色情、暴力、血腥图片自动检测。
- 完全免费开源，下载即用。

## 最新消息

- 🚀 v1.0 已发布，欢迎使用！

## 主要功能

- 快速生成图像
- 图像支持oss、cdn存储与加速服务
- 前端由uniapp构建，支持二开，一键发布多端。

## 开发计划

- [ ] 接入Stable Video Diffusion Image-to-Video 模型

## 最新动态

- 🚀 v1.0 支持自定义开启图片检测。

## 前端代码

> https://github.com/aiApplet/front-end

## 开始使用

1. 克隆项目

```shell
git clone https://github.com/aiApplet/back-end.git
```

2. 安装依赖

```shell
cd back-end
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. 修改配置文件

```shell
cd back-end
mkdir .env
```

```python
# 参考
# mysql 地址 示例：mysql://账号:密码@ip:端口/数据库昵称?charset=utf8mb4
DEFAULT_DATABASE = ''
# redis 示例：redis://:<your_redis_password>@<your_redis_host>:<your_redis_port>/<your_redis_db>  例：redis://127.0.0.1:6379/1
REDIS_LOCATION = ""
# 是否开启DEBUG
DEBUG = True
# Django的SECRET_KEY 有默认值
SECRET_KEY = ''
# 微信小程序的APPID和APPSECRET
APPID = ''
APP_SECRET = ''
# 阿里云OSS RAM KEY 和 SECRET
ALIYUN_KEY = ''
ALIYUN_SECRET = ''
# 阿里云的oss 域名配置
ALIYUN_HOST = ''
# 阿里云的oss BUCKET昵称
ALIYUN_BUCKET = ''
# 阿里云的oss ENDPOINT端点
ALIYUN_ENDPOINT = ''
# 阿里云的oss 内网ENDPOINT端点
ALIYUN_INTERNAL_ENDPOINT = ''
```

4. 初始化数据库

```shell
python manage.py makemigrations
python manage.py migrate
```

5. 创建管理员

```shell
python manage.py createsuperuser
```

6. 启动服务

```shell
python manage.py runserver 0.0.0.0:8000
```

## settings配置

### API文档配置

> SPECTACULAR_SETTINGS

> 参考 https://drf-spectacular.readthedocs.io/en/latest/settings.html

### 后台卡在登录 爆csrf错误

> 设置 CSRF_TRUSTED_ORIGINS = ["your_domain"]

### token 超时时间

> SIMPLE_JWT

### 签到奖励

> SIGN_IN_REWARD

### 邀请新用户奖励

> SHARE_NEW_USER

### 单次生图花费

> GEN_IMAGE_COST

### 新用户注册送积分

> REGISTER_NEW_USER_REWARD

### stablediffusion 配置

> STABLE_DIFFUSION_CONFIG

### 阿里云oss配置

> ALIYUN_OSS_CONFIG

### 是否开启OSS

> ALIYUN_OSS_ENABLE

### 是否开启图片自动审核 调用阿里云图片检测（要求oss和imm同时开启） 部分区域可用 参考 https://help.aliyun.com/document_detail/107743.html

> ENABLE_IMAGE_AUDIT

### 本地启动路径

> LOCAL_HOST = f"127.0.0.1:{8000 if DEBUG else 9999}"

## 要求

Python >= 3.10

## LICENSE

[AGPL-3.0](https://www.gnu.org/licenses/agpl-3.0.html)