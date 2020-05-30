#!/usr/bin/env python3
# -*- encoding:utf-8 -*-

import requests

# 微信消息通知
def send_msgwc(sckey,title,msg):
    endpoint = "https://sc.ftqq.com/" + sckey + ".send"
    dt = {"text": title, "desp": msg}
    r = requests.post(endpoint, data=dt)
    if r.status_code == 200:
        return 0
    else:
        return -1


