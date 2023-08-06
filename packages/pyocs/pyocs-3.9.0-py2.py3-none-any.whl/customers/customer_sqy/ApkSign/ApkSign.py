#! /usr/bin/python3
# -*- coding: utf-8 -*-


import requests


# import tempfile

#返回签名后的apk下载链接
def signApk(signType,apkPath):
    url = "http://10.22.30.101:8090/index"

    formData = dict()
    headers = dict()
    headers.update({
        'Origin': 'http://10.22.30.101:8090',
        'Connection': 'keep-alive',
        'Referer': 'http://10.22.30.101:8090/index'
        # 不能加这句话，否则无法传文件
        # 'Content-Type': 'multipart/form-data'
    })

    formData.update({
        'signer_type': signType,
        'fromWhere': 'app'
    })
    payload ={
    'file': (apkPath, open(apkPath, 'rb'), "application/octet-stream")
    }
    r = requests.post(url, data=formData, files=payload, headers=headers)
    return r.text


if __name__ == '__main__':
    pass