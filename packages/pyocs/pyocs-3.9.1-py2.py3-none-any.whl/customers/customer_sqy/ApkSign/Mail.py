import re
import os
from Constant import BASE_PATH

import poplib
import smtplib
import telnetlib
import email
import email.policy
from email.parser import Parser
from email.header import Header
from email.header import decode_header
from email.utils import parseaddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

class Mail():
    DEFAULF_POP3_SERVER = 'pop.cvte.com'
    DEFAULF_SMTP_SERVER = 'smtp.cvte.com'

    def __init__(self, mailAddr, mailPwd, pop3Server=DEFAULF_POP3_SERVER):
        self.mailAddr = mailAddr
        self.mailPwd = mailPwd
        self.pop3Server = pop3Server
        self.mailLogin()

    def mailLogin(self):
        try:
            telnetlib.Telnet(self.pop3Server, 995)
            #timeout参数设置的太小，容易报timeout的错误
            #报错：socket.timeout: The read operation timed out
            self.server = poplib.POP3_SSL(self.pop3Server, 995, timeout=80)
        except:
            time.sleep(5)
            self.server = poplib.POP3(self.pop3Server, 110, timeout=80)

        self.server.user(self.mailAddr)
        self.server.pass_(self.mailPwd)

    def __decode(self,s):
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value

    def getApkFromMail(self,mailID):
        ret = list()
        resp, lines, octets = self.server.retr(mailID)
        msgContent = b'\r\n'.join(lines).decode('utf-8','ignore')
        msg = Parser().parsestr(msgContent)
        for part in msg.walk():
            contentType = part.get_content_type()
            if 'application/octet-stream' not in contentType:
                continue
            filename = part.get_filename()
            if not filename:
                continue
            if 'apk' in filename:
                ret.append(os.path.join(BASE_PATH, filename))
                filedata = part.get_payload(decode=True)
                with open(os.path.join(BASE_PATH, filename),'wb+') as fp3:
                    fp3.write(filedata)
        return ret

    def getSpecialSubjectMail(self,specialMailSubject):
        resp, mails, octets = self.server.list()
        currMailNum = len(mails)
        print('当前邮箱中的邮件数量：' + str(currMailNum))
        MailRecordFile = os.path.join(BASE_PATH, 'tmp/MailRecord.txt')
        if os.path.exists(MailRecordFile):
            with open(MailRecordFile) as fp1:
                oldMailNum = int(fp1.readline().strip())
        for index in range(currMailNum,oldMailNum,-1):
            try:
                resp, lines, octets = self.server.retr(index)
                msg_content = b'\r\n'.join(lines).decode('utf-8','ignore')
                msg = Parser().parsestr(msg_content)
                mailSubject = self.__decode(msg.get('Subject',''))
                print(mailSubject)
                if specialMailSubject not in mailSubject:
                    continue
                with open(MailRecordFile,'w+',encoding="utf-8") as fp2:
                    print(str(index), file=fp2)
                return index
            except:
                continue
        with open(MailRecordFile,'w+',encoding="utf-8") as fp2:
            print(str(currMailNum), file=fp2)
        return -1

    def decodeMailAddr(self,s):
        ret = list()
        mail_addr_pattern = re.compile(r'<?(\w+@\w+\.\w+)>?')#匹配邮箱
        for item in decode_header(s):
            if item[-1]:
                continue
            try:
                #item[0]是byte类型，要转成string类型才能用正则匹配
                if type(item[0]) == bytes:
                    mail_addr = mail_addr_pattern.findall(item[0].decode())
                else:
                    mail_addr = mail_addr_pattern.findall(item[0])
                ret.extend(mail_addr)
            except:
                continue
        if ret:
            return ret
        value, charset = decode_header(s)[0]
        if charset:
            ret.append(value.decode(charset))
        return ret

    def getMailFromAddr(self,mailID):
        resp, lines, octets = self.server.retr(mailID)
        msgContent = b'\r\n'.join(lines).decode('utf-8','ignore')
        msg = Parser().parsestr(msgContent)
        return self.decodeMailAddr(msg.get('From',''))[0]

    def sendMailWithAttachment(self,mailToAddr,attachmentFileList):

        m = MIMEMultipart()
        m['Subject'] =  Header('【APK自动签名成功】', 'utf-8')
        m["From"] = Header(self.mailAddr)
        m["To"] = Header(mailToAddr)

        for attachmentFile in attachmentFileList:
            attatchmentPart = MIMEApplication(open(attachmentFile, 'rb').read())
            attatchmentPart.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachmentFile))
            m.attach(attatchmentPart)

        try:
            server = smtplib.SMTP(self.DEFAULF_SMTP_SERVER)
            server.login(self.mailAddr,self.mailPwd)
            server.sendmail(self.mailAddr, mailToAddr, m.as_string())
            print('success')
            server.quit()
        except smtplib.SMTPException as e:
            print('error:',e) #打印错误

if __name__ == '__main__':
    for i in range(2,2,-1):
        print(i)
