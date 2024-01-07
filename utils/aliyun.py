import base64
import datetime
import hmac
import json
from hashlib import sha1

import oss2
from django.conf import settings

from utils.utils import local_timestamp


class AliYunOSS:
    """阿里云 OSS 类"""

    OSS_ENDPOINT = settings.ALIYUN_OSS_CONFIG.get("end_point", None)
    OSS_INTERNAL_ENDPOINT = settings.ALIYUN_OSS_CONFIG.get("end_internal_point", None)
    # 账号
    OSS_KEY = settings.ALIYUN_OSS_CONFIG.get("key", None)
    # 密码
    OSS_SECRET = settings.ALIYUN_OSS_CONFIG.get("secret", None)
    OSS_HOST = settings.ALIYUN_OSS_CONFIG.get("host", None)
    OSS_BUCKET = settings.ALIYUN_OSS_CONFIG.get("bucket", None)
    INTERNAL = True

    def __init__(self, *args, **kwargs):
        self._auth = None
        self._service = None
        self._bucket = None

    @property
    def auth(self):
        if self._auth is None:
            self._auth = oss2.Auth(self.OSS_KEY, self.OSS_SECRET)
        return self._auth

    @property
    def service(self):
        if self._service is None:
            self._service = oss2.Service(self.auth, self.OSS_ENDPOINT)
        return self._service

    @property
    def bucket(self):
        if self._bucket is None:
            self._bucket = oss2.Bucket(
                self.auth,
                self.OSS_ENDPOINT if self.INTERNAL else self.OSS_INTERNAL_ENDPOINT,
                self.OSS_BUCKET,
            )
        return self._bucket

    @property
    def cdn_static_host(self):
        return settings.ALIYUN_OSS_CONFIG.get("cdn_static_host", None)

    @property
    def cdn_media_host(self):
        return settings.ALIYUN_OSS_CONFIG.get("cdn_media_host", None)

    def get_iso_8601(self, expire):
        return datetime.datetime.fromtimestamp(expire).isoformat() + "Z"

    def get_token(self):
        # 过期时间 存储路径
        expire_time, upload_dir = 300, "media/font_end/"
        expire_syncpoint = local_timestamp() + expire_time
        expire = self.get_iso_8601(expire_syncpoint)
        policy_dict = {
            "expiration": expire,
            "conditions": [["starts-with", "$key", upload_dir]],
        }

        policy_encode = base64.b64encode(json.dumps(policy_dict).strip().encode())
        h = hmac.new(self.OSS_SECRET.encode(), policy_encode, sha1)
        sign_result = base64.encodebytes(h.digest()).strip()

        token_dict = {
            "accessid": self.OSS_KEY,
            "host": self.OSS_HOST,
            "policy": policy_encode,
            "signature": sign_result,
            "expire": expire_syncpoint,
            "dir": upload_dir,
        }
        return token_dict


aliyun = AliYunOSS()


def upload_image(image_name, image_data):
    if not settings.DEBUG:
        aliyun.INTERNAL = False
    aliyun.bucket.put_object(image_name, image_data)
    return settings.ALIYUN_OSS_CONFIG["host"] + image_name
