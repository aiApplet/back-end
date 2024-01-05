#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author:anning
# @email:anningforchina@gmail.com
# @time:2024/01/05 22:27
# @file:stable_diffusion.py
import requests


class StableDiffusion:
    """Stable Diffusion模型"""

    def __init__(self):
        pass

    @staticmethod
    def generate_image(url, config):
        # 使用Stable Diffusion模型生成图像的代码
        # prompt是提示文本
        # 返回生成的图像
        response = requests.post(url=url, json=config, timeout=60)
        return response.json()
