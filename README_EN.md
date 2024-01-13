<div align="center">

# 🌟 Ai-applet 🌟

English / [Simplified Chinese](./README.md)

🎨 **Create stunning images with stable diffusion, boasting multi-cluster support and a central task scheduling hub.** 🚀

</div>
## Features 🌟

- 🖼️ Utilize stable diffusion for image generation, support for multiple machines, automatic scheduling.
- 💡 Clear development logic, no changes to stable diffusion source code, support for custom models, multi-cluster,
  multi-tasking, multi-user support.
- 🛠️ Built with DRF for API, simple code logic, easy to start.
- 🌐 Supports OSS upload, reducing bandwidth pressure.
- 🚫 Automatic detection for inappropriate content (nudity, violence, blood).
- 🎉 Completely free and open-source, ready to use upon download.

## Latest News 📢

- 🚀 v1.0 released, welcome to use! 🎊

## Main Functions

- Rapid image generation
- Image support for oss, CDN storage, and acceleration services
- Front-end built with uniapp, supports secondary development, and one-click multi-platform release.

## Development Plan

- [ ] Integration with Stable Video Diffusion Image-to-Video model

## Latest Updates

- 🚀 v1.0 supports custom activation of image detection.

## Front-end Code

> [https://github.com/aiApplet/front-end](https://github.com/aiApplet/front-end)

## Getting Started

1. Clone the project

```shell
git clone https://github.com/aiApplet/back-end.git
```

2. Installation dependency

```shell
cd back-end
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Modifying a configuration file

```shell
cd back-end
mkdir .env
```

```python
# Example
# MySQL address example: mysql://username:password@ip:port/database_nickname?charset=utf8mb4
DEFAULT_DATABASE = ''
# Redis example: redis://:<your_redis_password>@<your_redis_host>:<your_redis_port>/<your_redis_db>  Example: redis://127.0.0.1:6379/1
REDIS_LOCATION = ""
# Whether to enable DEBUG
DEBUG = True
# Django's SECRET_KEY has a default value
SECRET_KEY = ''
# WeChat Mini Program's APPID and APPSECRET
APPID = ''
APP_SECRET = ''
# Aliyun OSS RAM KEY and SECRET
ALIYUN_KEY = ''
ALIYUN_SECRET = ''
# Aliyun's oss domain configuration
ALIYUN_HOST = ''
# Aliyun's oss BUCKET nickname
ALIYUN_BUCKET = ''
# Aliyun's oss ENDPOINT
ALIYUN_ENDPOINT = ''
# Aliyun's oss internal ENDPOINT
ALIYUN_INTERNAL_ENDPOINT = ''
```

4. Initialize database

```shell
python manage.py makemigrations
python manage.py migrate
```

5. Create an administrator

```shell
python manage.py createsuperuser
```

6. Start service

```shell
python manage.py runserver 0.0.0.0:8000
```

## Settings Configuration

### API Documentation Configuration

> SPECTACULAR_SETTINGS

> Refer to https://drf-spectacular.readthedocs.io/en/latest/settings.html

### Backend Stuck at Login, CSRF Error

> Set CSRF_TRUSTED_ORIGINS = ["your_domain"]

### Token Expiry Time

> SIMPLE_JWT

### Sign-in Reward

> SIGN_IN_REWARD

### Invite New User Reward

> SHARE_NEW_USER

### Cost of Generating an Image

> GEN_IMAGE_COST

### New User Registration Reward

> REGISTER_NEW_USER_REWARD

### StableDiffusion Configuration

> STABLE_DIFFUSION_CONFIG

### Aliyun OSS Configuration

> ALIYUN_OSS_CONFIG

### Enable OSS

> ALIYUN_OSS_ENABLE

### Enable Automatic Image Review using Aliyun Image Detection (requires OSS and IMM to be enabled together) Available in some regions. Refer to https://help.aliyun.com/document_detail/107743.html

> ENABLE_IMAGE_AUDIT

### Local Startup Path

> LOCAL_HOST = f"127.0.0.1:{8000 if DEBUG else 9999}"

## requirements

Python >= 3.10

## LICENSE

[AGPL-3.0](https://www.gnu.org/licenses/agpl-3.0.html)