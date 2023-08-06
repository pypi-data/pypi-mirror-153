#! /usr/bin/python3
# -*- coding: utf-8 -*-
import os
import wget
from Mail import Mail
from ApkSign import signApk
from Constant import BASE_PATH

if __name__ == '__main__':
    m = Mail('account','passwd')
    mailID = m.getSpecialSubjectMail('【APK自动签名】')
    if mailID == -1:
        print("没有需要处理的\n")
    attachmentList = m.getApkFromMail(mailID)
    print(attachmentList)
    mailFromAddr = m.getMailFromAddr(mailID)
    print(mailFromAddr)

    signType = 'aml962x2'
    signedAPKList = list()
    for file in attachmentList:
        signedAPKDownloadUrl = signApk(signType,file)
        downLoadFileName = wget.download(signedAPKDownloadUrl, out=file.replace('.apk','') + '-' + signType +'-signed.apk')
        print('\n')
        signedAPKList.append(os.path.join(BASE_PATH, downLoadFileName))

    m.sendMailWithAttachment(mailFromAddr,signedAPKList)

    #step3 清尾，删除中间文件
    for i in attachmentList:
        os.remove(i)
    for i in signedAPKList:
        os.remove(i)
